import json
import requests

QUERY_ENDPOINT = "http://localhost:8080/search/"

headers = { "Content-Type" : "application/json" }
params = {
    "yql": """select * from sources doc where doc_title contains "COVID"; """,
    "hits": 10,
    "ranking.profile": "bm25"
}
resp = requests.get(QUERY_ENDPOINT, headers=headers, params=params)
print(json.dumps(resp.json(), indent=2))
