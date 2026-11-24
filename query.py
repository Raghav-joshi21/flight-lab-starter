"""Running queries against the flight database."""

import math

from validator import parse_datetime

RECORD_KEYS = (
    "flight_id","origin","destination","departure_datetime","arrival_datetime","price",
)
ALLOWED_KEYS =set(RECORD_KEYS) | {"min_price", "sort_by", "order", "limit"}
STRING_KEYS =("flight_id", "origin","destination")
DATETIME_KEYS =("departure_datetime","arrival_datetime")
NUMBER_KEYS =("price","min_price")

def _is_number(v) -> bool:
    return isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v) 
def _is_valid(query) -> bool:
    if not isinstance(query, dict):
        return False
    if not set(query) <= ALLOWED_KEYS:
        return False
    for k in STRING_KEYS:
        if k in query and not isinstance(query[k], str):
            return False
    for k in DATETIME_KEYS:
        if k in query and parse_datetime(query[k]) is None:
            return False 
    for k in NUMBER_KEYS:
        if k in query and not _is_number(query[k]):
            return False
    if "sort_by" in query:
        if not isinstance(query["sort_by"], str) or query["sort_by"] not in RECORD_KEYS:
            return False
    if "order" in query:
        if "sort_by" not in query:
            return False
        if not isinstance(query["order"], str) or query["order"] not in ("asc", "desc"):
            return False
    if "limit" in query:
        lim = query["limit"]
        if not isinstance(lim, int) or isinstance(lim, bool) or lim < 0:
            return False
    return True

def _matches(rec: dict, q: dict) -> bool:
    try:
        for k in STRING_KEYS:
            if k in q and rec[k] != q[k]:
                return False
        if "departure_datetime" in q and rec["departure_datetime"] < q["departure_datetime"]:
            return False
        if "arrival_datetime" in q and rec["arrival_datetime"]>q["arrival_datetime"]:
            return False
        if "price" in q and not rec["price"]<=q["price"]:
            return False
        if "min_price" in q and not rec["price"]>=q["min_price"]:
            return False
    except (KeyError, TypeError):
        return False
    return True

def run_query(db: list[dict], query: dict) -> dict:
    """Return one response entry for one query object"""
    if not _is_valid(query):
        return {"query": query, "error": "INVALID_QUERY", "matches": []}

    matches = [dict(r) for r in db if _matches(r, query)]
    if "sort_by" in query:
        key = query["sort_by"]
        try:
            matches = sorted(
                matches, key=lambda r: r[key], reverse=query.get("order") == "desc"
            )
        except (KeyError, TypeError):
            pass
    if "limit" in query:
        matches = matches[: query["limit"]]
    return {"query": query, "matches": matches}

def run_queries(db: list[dict], queries: dict | list) -> list[dict]:
     """Accept one query object or a list of them; always return a list."""
     if isinstance(queries, list):
        return [run_query(db, q) for q in queries]
     return [run_query(db, queries)]
