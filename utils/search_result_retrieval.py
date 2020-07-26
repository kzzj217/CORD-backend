import os
import os.path as osp
from utils import file_utils, const
import json

def retrieve_answer(query, root):
    file_utils.create_folder(root)
    path = osp.join(root, "answer.json")
    #os.system("curl --header \"Content-Type: application/json\" --request POST --data \'{\"question\" : \"%s\", \"section\" : \"\"}\' http://cslab241.cs.aueb.gr:5000/just_the_json > %s "%(query, path))

    return json.load(open(path))

def get_answer_dois(articles):
    return [article['doi'] for article in articles]