import json
import numpy as np
import os
import pandas as pd
import requests

SCHEMA = "vespa-poc"
ENDPOINT = "http://localhost:8080/document/v1/" + SCHEMA + "/doc/docid/{:d}"

DATA_DIR = "../../../../2021-02-01"

METADATA_FILE = os.path.join(DATA_DIR, "metadata.csv")
EMBEDDING_FILE = os.path.join(DATA_DIR, "cord_19_embeddings_2021-02-01.csv")

print("reading metadata...")
metadata_df = pd.read_csv(METADATA_FILE)
metadata_df = (
    metadata_df[["cord_uid", "title", "abstract"]]
    .dropna()
    .drop_duplicates()
)
metadata_df = metadata_df.set_index("cord_uid")
print(metadata_df.head())

successes, failures = 0, 0
headers = { "Content-Type": "application/json" }
print("reading embeddings...")
femb = open(EMBEDDING_FILE, "r")
for doc_id, line in enumerate(femb):
    # if doc_id + 1 % 1000 == 0:
    #     print("{:d} documents read, {:d} succeeded, {:d} failed"
    #         .format(doc_id + 1, successes, failures))
    cols = line.strip().split(',')
    cord_uid = cols[0]
    specter_vec = [float(x) for x in cols[1:]]
    try:
        lookup_rec = metadata_df.loc[cord_uid]
        if not isinstance(lookup_rec["title"], str) and lookup_rec["title"].count() > 1:
            title = lookup_rec.iloc[0]["title"]
            abstract = lookup_rec.iloc[0]["abstract"]
        else:
            title = lookup_rec["title"]
            abstract = lookup_rec["abstract"]
    except KeyError:
        continue
    input_rec = {
        "fields": {
            "cord_uid": cord_uid,
            "doc_title": title,
            "doc_abstract": abstract,
            "specter_embedding": {
                "values": specter_vec
            }
        }
    }
    # print(json.dumps(input_rec, indent=2))
    url = ENDPOINT.format(doc_id)
    resp = requests.post(url, headers=headers, json=input_rec)
    if resp.status_code != 200:
        print("ERROR loading [{:s}]: {:s}".format(cord_uid, resp.reason))
        failures += 1
    else:
        successes += 1
    print("Inserted document {:s}, {:d} ok, {:d} failed, {:d} total\r"
        .format(cord_uid, successes, failures, doc_id + 1), end="")

print("\n{:d} documents read, {:d} succeeded, {:d} failed, COMPLETE"
    .format(doc_id + 1, successes, failures))

femb.close()
