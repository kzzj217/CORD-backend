import os.path as osp
#root = "/Users/zijinkong/Desktop/Covid-19/CORD-19/"
root='/mnt/d/workfolder/RA/CORD-19/'
root_path = osp.join(root, '../CORD-19-research-challenge')
ANS_CACHE_ROOT = osp.join(root, "./database/ans_cache")

DB_CACHE = osp.join(root, "./database/database.pkl")
DB_SAMPLE_CACHE = osp.join(root, "./database/sample.pkl")

ABSTAG_JSON_CACHE = osp.join(root, "./database/sample.json")
ABSTAG_METHOD = ["sciwing"]
