import json
import nltk
import numpy as np
import re
import requests

from nltk.corpus import stopwords

SCHEMA_NAME = "vespa-poc/doc"

GET_ENDPOINT_URL = "http://localhost:8080/document/v1/" + SCHEMA_NAME + "/docid/{:d}"
SEARCH_ENDPOINT_URL = "http://localhost:8080/search/"

stop_words = set(stopwords.words('english'))

headers = { "Content-Type" : "application/json" }
resp = requests.get(GET_ENDPOINT_URL.format(437375), headers=headers)
resp_json = resp.json()
title = resp_json["fields"]["doc_title"]
emb = np.zeros((768), dtype=np.float32)
for cell in resp_json["fields"]["specter_embedding"]["cells"]:
    pos = int(cell["address"]["x"])
    val = cell["value"]
    emb[pos] = val

title_words = list(set([word for word in title.split() if word.lower() not in stop_words]))
title_part = " or ".join(["doc_title contains '{:s}'".format(w) for w in title_words])

params = {
    "yql": """select * from sources doc where ([{"targetHits": 10}]nearestNeighbor(specter_embedding, query_vector)) and (%s); """ % (title_part),
    "hits": 100,
    "ranking.features.query(query_vector)": emb.tolist(),
    "ranking.profile": "semantic-similarity"
}

data = json.dumps(params, indent=2)
resp = requests.post(SEARCH_ENDPOINT_URL, headers=headers, data=data)
if resp.status_code != 200:
    print("Error ({:d}): {:s}".format(resp.status_code, resp.reason))
else:
    resp_json = resp.json()
    num_hits = resp_json["root"]["fields"]["totalCount"]
    for rec in resp_json["root"]["children"]:
        # print(rec)
        id = rec["id"]
        relevance = rec["relevance"]
        cord_uid = rec["fields"]["cord_uid"]
        title = rec["fields"]["doc_title"]
        abstract = rec["fields"]["doc_abstract"]
        print("\t".join([cord_uid, title, str(relevance)]))

# print(json.dumps(json.loads(resp.text), indent=2))

