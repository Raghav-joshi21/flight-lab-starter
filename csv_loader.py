"""Reading CSV files into flight records and error messages."""
import csv
import os

from validator import to_record, validate_row 

def parse_files(paths: list[str], airports: set[str]) -> tuple[list[dict], list[str]]:
    """Process files in order; return (valid records,error messages)."""
    records: list[dict] = []
    errors: list[str] = []
    seen: set[tuple[str, str]] = set() #give flight is and departure of valid records to check for duplicates

    for path in paths:
        name = os.path.basename(path)
        with open(path, encoding="utf-8-sig", newline=None) as f:
            for lineno, raw in enumerate(f, start=1):
                if lineno == 1:
                    continue  # header
                line = raw.rstrip("\r\n")
                stripped = line.strip()
                if not stripped or stripped.startswith("#"):
                    continue
                #split the line into fields using csv.reader which handles quoted commas
                try:
                    fields = next(csv.reader([line]))
                except (csv.Error, StopIteration):
                    errors.append(f"{name}:{lineno}: WRONG_FIELD_COUNT | {stripped}")
                    continue

                code = validate_row(fields, airports)
                if code is None:
                    #record is valid check for duplicates and add to records if not duplicate
                    record = to_record(fields)
                    key = (record["flight_id"], record["departure_datetime"])
                    if key in seen:
                        code = "DUPLICATE_FLIGHT"
                    else:
                        seen.add(key)
                        records.append(record)
                        continue
                errors.append(f"{name}:{lineno}: {code} | {stripped}")
    return records, errors