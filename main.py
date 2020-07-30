import uvicorn
from fastapi import FastAPI, UploadFile
from schemas import *
import pickle
from utils import search_result_retrieval, const, conversion
import os, boto3
from starlette.middleware.cors import CORSMiddleware
from io import BytesIO
import json

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def load_data():
    print("LOAD DATABASE FROM AWS S3 SYSTEM...")
    S3_BUCKET = os.environ.get("S3_BUCKET")
    print("S3 bucket", S3_BUCKET)

    s3 = boto3.resource('s3')
    with BytesIO() as data:
        s3.Bucket('wingnuscord19').download_fileobj(const.DEMO_DB_CACHE, data)
        data.seek(0)
        database = pickle.load(data)

    with BytesIO() as data:
        s3.Bucket('wingnuscord19').download_fileobj(const.DEMO_ABSTAG_CACHE, data)
        data.seek(0)
        db_abstags = json.load(data)

    with BytesIO() as data:
        s3.Bucket('wingnuscord19').download_fileobj(const.DEMO_GE_CACHE, data)
        data.seek(0)
        db_genericheader = json.load(data)

    with BytesIO() as data:
        s3.Bucket('wingnuscord19').download_fileobj(const.DEMO_I2B2_NER_CACHE, data)
        data.seek(0)
        db_i2b2ner = json.load(data)

    with BytesIO() as data:
        s3.Bucket('wingnuscord19').download_fileobj(const.DEMO_SIMILAR_CACHE, data)
        data.seek(0)
        db_similarpapers = json.load(data)

    with BytesIO() as data:
        s3.Bucket('wingnuscord19').download_fileobj(const.GRAPH_RISK_FACTOR, data)
        data.seek(0)
        graph_risk_factor = json.load(data)

    with BytesIO() as data:
        s3.Bucket('wingnuscord19').download_fileobj(const.GRAPH_STUDY_TYPE, data)
        data.seek(0)
        graph_study_type = json.load(data)

    return database, db_abstags, db_genericheader, db_i2b2ner, db_similarpapers, graph_risk_factor, graph_study_type

database, db_abstags, db_genericheader, db_i2b2ner, db_similarpapers, graph_risk_factor, graph_study_type = load_data()

"""
database = pickle.load(open(const.DEMO_DB_CACHE, 'rb'))
db_abstags = json.load(open(const.DEMO_ABSTAG_CACHE, 'r'))
db_genericheader = json.load(open(const.DEMO_GE_CACHE, 'r'))
db_i2b2ner = json.load(open(const.DEMO_I2B2_NER_CACHE, 'r'))
db_similarpapers = json.load(open(const.DEMO_SIMILAR_CACHE, 'r'))
#db_graph = json.load(open(const.DEMO_GRAPH_CACHE, 'r'))
graph_risk_factor = json.load(open(const.GRAPH_RISK_FACTOR, 'r'))
graph_study_type = json.load(open(const.GRAPH_STUDY_TYPE, 'r'))
"""

@app.get("/answer/", response_model=List[GeneralAns])
def answer_query(query: str, limit = 20):
    ans = search_result_retrieval.retrieve_answer(query)
    print("Retrieve answers successfully.")
    result = []
    filtered_ans = search_result_retrieval.combine(ans)
    for note in filtered_ans:
        doi = note["doi"]
        # TODO: doi could be empty
        idx = database.loc[database['doi'] == doi].index
        if len(idx) is 0:
            print("ERROR: no corresponding DOI: ", doi, "Skip this answer")
            continue

        row = database.iloc[idx[0]]
        # TODO: abstag use both doi and paper id
        if not row["paper_id"] or row["paper_id"] not in db_abstags:
            abstags = {"sciwing": [""]*len(row["abstract"])}
        else:
            abstags = db_abstags[row["paper_id"]]

        if not row["paper_id"] or row["paper_id"] not in db_i2b2ner:
            i2b2tags = {"sciwingI2B2": {}}
        else:
            i2b2tags = db_i2b2ner[row["paper_id"]]

        if not row["paper_id"] or row["paper_id"] not in db_genericheader:
            genericHeader = [""]*len(row["body_text"])
        else:
            genericHeader = db_genericheader[row["paper_id"]]

        result.append(conversion.to_general_ans(note, row, abstags, i2b2tags, genericHeader))
    return result

@app.get("/compare/", response_model=Graph)
def get_graph(y: str):
    x="Publish Time"

    if y == "Study Type":
        return graph_study_type
    elif y == "Risk Factor":
        return graph_risk_factor
"""
    res = conversion.to_graph(database, db_graph['+'.join([x,y])], db_abstags, db_i2b2ner, db_genericheader)
    return res
"""

@app.get("/similar/{paper_id}", response_model=List[PaperInfo])
def get_similar_articles(paper_id: str):
    print("check similar papers")
    if paper_id in db_similarpapers.keys():
        similars = db_similarpapers[paper_id]

    else:
        similars = None

    return conversion.to_similar(database, similars, db_abstags, db_i2b2ner, db_genericheader)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    uvicorn.run("main:app", port=port, host='0.0.0.0', reload=True, log_level="info")