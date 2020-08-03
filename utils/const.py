import os.path as osp

root = "/Users/zijinkong/Desktop/Covid-19/CORD-19/"
ABSTAG_METHOD = ["sciwing", "coda19"]

DEMO_DB_CACHE = osp.join(root, "./database/demo_db.pkl")
DEMO_ABSTAG_CACHE = osp.join(root, "./database/demo_abstags.json")
DEMO_GE_CACHE = osp.join(root, "./database/demo_ge.json")
DEMO_I2B2_NER_CACHE = osp.join(root, "./database/demo_i2b2ner.json")
DEMO_SIMILAR_CACHE = osp.join(root, "./database/demo_similar.json")
DEMO_GRAPH_CACHE = osp.join(root, "./database/demo_graph.json")
GRAPH_STUDY_TYPE = osp.join(root, "./database/graph_Study_Type.json")
GRAPH_RISK_FACTOR = osp.join(root, "./database/graph_Risk_Factor.json")

root_path = osp.join(root, '../CORD-19-research-challenge')
ANS_CACHE_ROOT = osp.join(root, "./database/ans_cache")

DB_CACHE = osp.join(root, "./database/database.pkl")
ABSTAG_JSON_CACHE = osp.join(root, "./database/abstags.json")
GenericHeader_JSON_CACHE = osp.join(root, "./database/generic_headers.json")
SciwingI2B2_NER_CACHE = osp.join(root, "./database/i2b2ner.json")
SIMILAR_CACHE = osp.join(root, "./database/similar.pkl")

XTYPEs = ["Date"]
YTYPEs = ["Risk Factor"]

DEMO_DB_CACHE = "demo_db.pkl"
DEMO_ABSTAG_CACHE = "demo_abstags.json"
DEMO_GE_CACHE = "demo_ge.json"
DEMO_I2B2_NER_CACHE = "demo_i2b2ner_v2.json"
DEMO_SIMILAR_CACHE = "demo_similar.json"
GRAPH_STUDY_TYPE = "graph_Study_Type.json"
GRAPH_RISK_FACTOR = "graph_Risk_Factor.json"
