import uvicorn
from fastapi import FastAPI
from schemas import *
import pickle
from utils import search_result_retrieval, const, conversion
import json
from starlette.middleware.cors import CORSMiddleware

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8000",
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


database = pickle.load(open(const.DB_SAMPLE_CACHE, 'rb'))
abstags = json.load(open(const.ABSTAG_JSON_CACHE, 'rb'))

@app.get("/answer/", response_model=List[Answer])
def answer_query(query: str, limit = 20):
    ans = search_result_retrieval.retrieve_answer(query, const.ANS_CACHE_ROOT)
    print("Retrieve answers successfully.")
    ans = conversion.to_ans(ans)
    return ans

@app.get("/answer/abstract", response_model=Abstract)
def expand_abs(doi: str):
    # dummy doi
    doi = "10.1292/jvms.13-0518"
    row = database.loc[database['doi'] == doi]
    # TODO: ensure the existence
    tags = abstags[row["paper_id"].values[0]]
    abs = conversion.to_abstract(row, tags)
    return abs

@app.get("/answer/paper/{paper_id}", response_model=Paper)
def read_paper(paper_id: str):
    paper = database.loc[database['paper_id']==paper_id]
    return {"paper_id": paper_id,
            "title": "what is covid-19",
            "author": "Jack",
            "abstract": str(paper['abstract'].values),
            "body_text": str(paper['body_text'].values)}

@app.get("/display", response_model=List[Paper])
def display():
    print("CALL FROM FRONTEND")
    #print(type(json.load(open(all_json[0], "rb"))))
    #return json.load(open(all_json[0], "rb"))


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)