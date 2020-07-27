import uvicorn
from fastapi import FastAPI
from schemas import *
import pickle
from utils import search_result_retrieval, const, conversion
import json
from starlette.middleware.cors import CORSMiddleware
import random

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://3.17.70.182",
    "http://192.168.1.132/",
	'http://192.168.2.121/'
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

print("LOADING database...")
#database = pickle.load(open(const.DB_CACHE, 'rb'))
#database = pickle.load(open(const.DB_SAMPLE_CACHE, 'rb'))
print("LOADING db_abstags...")
#db_abstags = json.load(open(const.ABSTAG_JSON_CACHE, 'r'))
print("LOADING bodytext I2B2 NER...")
#db_i2b2ner = json.load(open(const.SciwingI2B2_NER_CACHE, 'r'))
print("LOADING similar papers...")
#db_similarpapers = pickle.load(open(const.SIMILAR_CACHE, 'rb'))
print("LOADING generic headers...")
#db_genericheader = json.load(open(const.GenericHeader_JSON_CACHE, 'r'))

@app.get("/answer/", response_model=List[GeneralAns])
def answer_query(query: str, limit = 20):
    ans = search_result_retrieval.retrieve_answer(query, const.ANS_CACHE_ROOT)
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

@app.get("/compare/{x}+{y}", response_model=Graph)
def get_graph(x: str, y: str):
    # TODO:change stub
    db_abstags = []
    Xaxis = ["RiskFactor1", "RF2", "RF3"]
    Yaxis = ["TimeInterval1", "TI2", "TI3"]
    values = dict()
    for x in Xaxis:
        for y in Yaxis:
            values[(x, y)] = database.sample(n=int(random.random()*len(database)))

    # include all tags
    res = conversion.to_graph(x, y, Xaxis, Yaxis, values, db_abstags)
    return res

@app.get("/answer/{paper_id}", response_model=List[PaperInfo])
def get_similar_articles(paper_id: str):
    print("check similar papers")
    if paper_id in db_similarpapers.keys():
        similars = db_similarpapers[paper_id]

    else:
        similars = None

    return conversion.to_similar(similars, db_abstags, db_i2b2ner, db_genericheader)

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    uvicorn.run("main:app", port=5000, host='180.129.116.124', reload=True, log_level="info")