from typing import Optional
from fastapi import FastAPI

import demo_utils


app = FastAPI()

@app.get("/")
def get_root():
    return {
        "message": "API for My Vespa POC",
        "documentation": "/docs"
    }


@app.get("/search")
def search_api(query: str, title_only: bool, start: int = 0, rows: int = 10):
    try:
        rows = demo_utils.do_search(query, title_only, start, rows)
        return {
            "params": {
                "query": query,
                "title_only": title_only,
                "start": start,
                "rows": rows
            },
            "status": "ok",
            "payload": rows
        }
    except Exception as e:
        return {
            "params": {
                "query": query,
                "title_only": title_only,
                "start": start,
                "rows": rows
            },
            "status": "error",
            "payload": str(e)
        }


@app.get("/mlt")
def mlt_api(doc_id: str, num_similar: int = 10):
    try:
        doc_title, rows = demo_utils.do_mlt(doc_id, num_similar)
        return {
            "params": {
                "doc_id": doc_id,
                "num_similar": num_similar,
            },
            "status": "ok",
            "doc_title": doc_title,
            "payload": rows
        }
    except Exception as e:
        return {
            "params": {
                "doc_id": doc_id,
                "num_similar": num_similar,
            },
            "status": "error",
            "payload": str(e)
        }
