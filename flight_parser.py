"""Flight Schedule Parser and Query Tool - command-line entry point.

Run from the project folder, for example:
    python flight_parser.py -i data/db.csv -a data/airports.txt
"""
import argparse
import json
import logging
import os
import sys
from datetime import datetime

from csv_loader import parse_files
from query import run_queries
from validator import load_airports


# TODO: fill in your details: plain ASCII, no spaces or underscores.
STUDENT_ID = "251ADB004"
FIRST_NAME = "Raghav"
LAST_NAME = "Joshi"

def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="flight_parser.py",
        description="Validate flight CSV files, build a JSON database, run queries.",
    )
    p.add_argument("-i", metavar="FILE", help="parse a single CSV file")
    p.add_argument("-d", metavar="FOLDER", help="parse every .csv file in a folder")
    p.add_argument("-j", metavar="FILE", help="load an existing JSON database")
    p.add_argument("-a", metavar="FILE", help="airport list file (needed with -i/-d)")
    p.add_argument("-o", metavar="FILE", help="output JSON database (default db.json)")
    p.add_argument("-q", metavar="FILE", help="JSON file with queries to run")
    p.add_argument("-r", metavar="FOLDER", default=".", help="folder for the response file")
    return p

def _load_json(path: str):
    with open(path, encoding="utf-8-sig") as f:
        return json.load(f)


def _write_json(path: str, data) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")


def _write_errors_log(log_path: str, errors: list[str], n_files: int, n_valid: int) -> None:
    logger = logging.getLogger("flight_parser")
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler(log_path, mode="w", encoding="utf-8")
    handler.setFormatter(
        logging.Formatter("%(asctime)s %(levelname)s %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
    )
    logger.addHandler(handler)
    try:
        logger.info("Processed %d file(s): %d valid, %d invalid", n_files, n_valid, len(errors))
        for message in errors:
            logger.warning(message)
    finally:
        logger.removeHandler(handler)
        handler.close()

def _run(args, parser) -> int:
    # usage errors -> exit code 2
    sources = [s for s in (args.i, args.d, args.j) if s is not None]
    if len(sources) == 0:
        parser.error("one data source is required: -i, -d or -j")
    if len(sources) > 1:
        parser.error("use only one of -i, -d, -j")
    if args.j is None and args.a is None:
        parser.error("-a is required with -i and -d")
    if args.j is not None and args.o is not None:
        parser.error("-o cannot be used with -j")

# load queries first, so a bad query file fails before anything is written
    queries = None
    if args.q is not None:
        queries = _load_json(args.q)
        if not isinstance(queries, (dict, list)):
            raise ValueError(f"{args.q}: query file must be an object or an array")

    # get the database: from -j, or by parsing -i / -d
    if args.j is not None:
        db = _load_json(args.j)
        if not isinstance(db, list) or not all(isinstance(r, dict) for r in db):
            raise ValueError(f"{args.j}: database must be a JSON array of objects")
    else:
        airports = load_airports(args.a)
        if args.i is not None:
            if not os.path.isfile(args.i):
                raise FileNotFoundError(f"file not found: {args.i}")
            paths = [args.i]
        else:
            if not os.path.isdir(args.d):
                raise FileNotFoundError(f"folder not found: {args.d}")
            names = sorted(
                n for n in os.listdir(args.d)
                if n.endswith(".csv") and os.path.isfile(os.path.join(args.d, n))
            )
            if not names:
                raise FileNotFoundError(f"no .csv files in folder: {args.d}")
            paths = [os.path.join(args.d, n) for n in names]

        db, errors = parse_files(paths, airports)
        out = args.o if args.o is not None else "db.json"
        log_path = os.path.join(os.path.dirname(os.path.abspath(out)), "errors.log")
        _write_json(out, db)
        _write_errors_log(log_path, errors, len(paths), len(db))
        print(f"{len(db)} valid flight(s), {len(errors)} invalid row(s)")

    # run queries and write exactly one response file
    if queries is not None:
        results = run_queries(db, queries)
        stamp = datetime.now().strftime("%Y%m%d_%H%M")
        name = f"response_{STUDENT_ID}_{FIRST_NAME}_{LAST_NAME}_{stamp}.json"
        _write_json(os.path.join(args.r, name), results)
        print(f"{len(results)} query result(s) written to {name}")

    return 0


def main(argv: list[str] | None = None) -> int:
    """Run the whole program and return the exit code (0, 1 or 2).

    argv is the argument list without the program name.
    None means use sys.argv[1:] (argparse does this for you).
    Do not call sys.exit() inside main(); return the code instead.
    """
    parser = _build_parser()
    try:
        args = parser.parse_args(argv)
        return _run(args, parser)
    except SystemExit as e:  # argparse usage errors and -h
        return e.code if isinstance(e.code, int) else (0 if e.code is None else 2)
    except (OSError, ValueError) as e:  # missing files, bad JSON
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:  # safety net: never show a traceback
        print(f"Error: {type(e).__name__}: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
