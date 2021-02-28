import json
import numpy as np
import requests

QUERY_ENDPOINT = "http://localhost:8080/search/"
DOC_ENDPOINT = "http://localhost:8080/document/v1/vespa-poc/doc/docid/{:d}"

def do_search(query, title_only, start_row, num_rows):
    headers = { "Content-Type" : "application/json" }
    if title_only:
        params = {
            "yql" : """
                select * from sources doc 
                where doc_title contains '{:s}' 
                limit {:d} 
                offset {:d};
            """.format(query.lower(), num_rows, start_row),
            "hits" : num_rows,
            "ranking.profile": "bm25"
        }
    else:
        params = {
            "yql": """
                select * from sources doc 
                where (doc_title contains '{:s}' or doc_abstract contains '{:s}')
                limit {:d} 
                offset {:d};
            """.format(query.lower(), query.lower(), num_rows, start_row),
            "query": query.lower(),
            "type": "any",
            "hits": num_rows,
            "ranking.profile": "bm25"
        }
    resp = requests.get(QUERY_ENDPOINT, headers=headers, params=params)
    resp_json = resp.json()
    # print("resp_json:", json.dumps(resp_json, indent=2))
    rows = []
    if resp_json["root"]["fields"]["totalCount"] > 0:
        for child in resp_json["root"]["children"]:
            row = {
                "relevance": child["relevance"],
                "doc_id": child["fields"]["documentid"],
                "cord_uid": child["fields"]["cord_uid"],
                "doc_title": child["fields"]["doc_title"],
                "doc_abstract": child["fields"]["doc_abstract"][0:248] + "..."
            }
            rows.append(row)
    return rows


def do_mlt(doc_id, num_similar):
    headers = { "Content-Type" : "application/json" }
    # get the vector for the specified doc ID
    docid = int(doc_id.split("::")[-1])
    resp = requests.get(DOC_ENDPOINT.format(docid), headers=headers)
    resp_json = resp.json()
    # print("resp_json:", json.dumps(resp_json, indent=2))

    doc_title = resp_json["fields"]["doc_title"]
    doc_vec = np.zeros((768), dtype=np.float32)
    for cell in resp_json["fields"]["specter_embedding"]["cells"]:
        pos = int(cell["address"]["x"])
        val = cell["value"]
        doc_vec[pos] = val

    # compose nearest neighbor query using doc vector and return results
    params = {
        "yql": """
            select * from sources doc
            where (
                [{"targetHits": 10}]
                nearestNeighbor(specter_embedding, query_vector));""",
        "hits": 100,
        "ranking.features.query(query_vector)": doc_vec.tolist(),
        "ranking.profile": "semantic-similarity" 
    }
    data = json.dumps(params)
    resp = requests.post(QUERY_ENDPOINT, headers=headers, data=data)
    if resp.status_code != 200:
        raise ValueError("Error {:d}: {:s}".format(resp.status_code, resp.reason))
    resp_json = resp.json()
    rows = []
    if resp_json["root"]["fields"]["totalCount"] > 0:
        for child in resp_json["root"]["children"]:
            row = {
                "relevance": child["relevance"],
                "doc_id": child["fields"]["documentid"],
                "cord_uid": child["fields"]["cord_uid"],
                "doc_title": child["fields"]["doc_title"],
                "doc_abstract": child["fields"]["doc_abstract"][0:248] + "..."
            }
            rows.append(row)

    return doc_title, rows