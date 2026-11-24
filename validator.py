"""Row validation: airport list loading, single-row checks, record building."""
import math
import re
from datetime import datetime

FLIGHT_ID_RE = re.compile(r"[A-Za-z0-9]{2,8}")
AIRPORT_RE = re.compile(r"[A-Z]{3}")
DATETIME_RE = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}")
DATETIME_FORMAT = "%Y-%m-%d %H:%M"

def load_airports(path: str) ->set[str]:
    """Read an airport list file and return the set of codes"""
    codes: set[str] =set()
    with open(path, encoding="utf-8-sig") as f:
        for line in f:
            code=line.strip()
            if not code or code.startswith("#"):
                continue
            codes.add(code)
    return codes

    
def parse_datetime(value: str) -> datetime | None:
    """Parse exactly 'YYYY-MM-DD HH:mm'(ASCII digit zero padded)"""
    if not isinstance(value, str) or not DATETIME_RE.fullmatch(value):
        return None
    try:
        return datetime.strptime(value, DATETIME_FORMAT)
    except ValueError:
        return None


def _parse_price(value: str)->float | None:
    """Return a finite float, or None if conversion fails or is not finite."""
    try:
        price=float(value)
    except (ValueError,OverflowError):
        return None
    return price if math.isfinite(price) else None

def validate_row(fields: list[str], airports: set[str]) -> str | None:

    """Check one CSV row (fields as returned by csv.reader, not yet stripped)"""
    if len(fields)!=6:
        return "WRONG_FIELD_COUNT"

    f =[x.strip() for x in fields]
    flight_id, origin,destination,departure,arrival, price =f
    if any(x == "" for x in f):
        return "MISSING_FIELD"
    if not FLIGHT_ID_RE.fullmatch(flight_id):
        return "INVALID_FLIGHT_ID"
    if not AIRPORT_RE.fullmatch(origin) or origin not in airports:
        return "INVALID_ORIGIN"
    if not AIRPORT_RE.fullmatch(destination) or destination not in airports:
        return "INVALID_DESTINATION"
    if origin == destination:
        return "SAME_ORIGIN_DESTINATION"
    dep = parse_datetime(departure)
    if dep is None:
        return "INVALID_DEPARTURE"
    arr = parse_datetime(arrival)
    if arr is None:
        return "INVALID_ARRIVAL"
    if arr <= dep:
        return "ARRIVAL_NOT_AFTER_DEPARTURE"
    value = _parse_price(price)
    if value is None:
        return "INVALID_PRICE"
    if value <= 0:
        return "NON_POSITIVE_PRICE"
    return None



def to_record(fields: list[str]) -> dict:
     """Turn a valid row into a flight record dictionary."""
     flight_id, origin, destination,departure, arrival, price = (
        x.strip() for x in fields
    )
     return {
        "flight_id": flight_id,
        "origin": origin,
        "destination": destination,
        "departure_datetime": departure,
        "arrival_datetime": arrival,
        "price": float(price),
    }
