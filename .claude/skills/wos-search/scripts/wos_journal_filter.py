#!/usr/bin/env python3
"""Query the ABS Academic Journal Guide 2024 Excel file and output WoS journal filters.

Usage:
  wos_journal_filter.py --list-fields
  wos_journal_filter.py --list-ratings
  wos_journal_filter.py --fields "INFO MAN" --ratings 4 "4*" --format so
  wos_journal_filter.py --fields ALL --ratings 4 "4*" --format count
"""

import argparse
import os
import re
import sys

try:
    import openpyxl
except ImportError:
    sys.stderr.write(
        "openpyxl is required. Install it with: pip3 install openpyxl\n"
    )
    sys.exit(1)

# --- Journal Name Cleaning ---

# Mapping of journals whose official WoS title uses "&" but ABS lists with "and".
# Key: ABS title (lowercased). Value: WoS-correct title.
AND_TO_AMPERSAND_MAP: dict[str, str] = {}
_ampersand_entries = [
    # Simple "and" → "&" replacements
    "Behaviour and Information Technology",
    "Cognition, Technology and Work",
    "Computers and Industrial Engineering",
    "Computers and Operations Research",
    "Group and Organization Management",
    "Industrial Management and Data Systems",
    "Information and Management",
    "Information Processing and Management",
    "Information Technology and People",
    "International Journal of Operations and Production Management",
    "Manufacturing and Service Operations Management",
    "Organization and Environment",
    "Psychology and Marketing",
    "R and D Management",
    "Technology Analysis and Strategic Management",
    "Total Quality Management and Business Excellence",
    "Work and Stress",
]
for _entry in _ampersand_entries:
    _corrected = _entry.replace(" and ", " & ").replace("R & D", "R&D")
    AND_TO_AMPERSAND_MAP[_entry.lower()] = _corrected

# Journals requiring more than a simple "and" → "&" substitution
_extra_mappings = {
    # ABS: "Science Technology and Human Values"
    # WoS:  "Science, Technology, & Human Values" (adds commas + &)
    "science technology and human values": "Science, Technology, & Human Values",
}
AND_TO_AMPERSAND_MAP.update(_extra_mappings)


def clean_journal_name(raw_title: str) -> str:
    """Clean a journal title to match the WoS source publication name.

    1. Strips parenthetical content (ABS disambiguators, abbreviations,
       translations, historical notes) — these are not part of the WoS title.
    2. Replaces "and" with "&" for journals whose official WoS title uses
       the ampersand form.
    """
    title = raw_title.strip()

    # Remove parenthetical content: abbreviations like (JASIST), location
    # disambiguators like (UK)/(USA)/(United Kingdom)/(Bingley), historical
    # notes like (previously ...), translations like (German Journal of ...),
    # and foreign titles like (Revista de ...).  All of these are ABS metadata
    # and not part of the WoS source publication name.
    title = re.sub(r"\s*\([^)]*\)", "", title)

    # Apply known "and" → "&" corrections (case-insensitive match)
    key = title.lower()
    if key in AND_TO_AMPERSAND_MAP:
        title = AND_TO_AMPERSAND_MAP[key]

    return title

# --- Constants ---
EXCEL_FILENAME = "ABS2024.xlsx"
SHEET_NAME = "Sheet1"
DATA_START_ROW = 3  # 1-indexed, row 1=title, row 2=headers

RATING_ORDER = {"4*": 0, "4": 1, "3": 2, "2": 3, "1": 4}


def find_excel_path(script_dir: str) -> str:
    """Resolve the path to ABS2024.xlsx."""
    # Check script directory first, then CWD
    candidates = [
        os.path.join(script_dir, "..", "..", "..", "..", EXCEL_FILENAME),
        os.path.join(os.getcwd(), EXCEL_FILENAME),
    ]
    for path in candidates:
        normalized = os.path.normpath(path)
        if os.path.isfile(normalized):
            return normalized
    sys.stderr.write(
        f"Could not find {EXCEL_FILENAME}. Looked in:\n"
        + "\n".join(f"  {os.path.normpath(p)}" for p in candidates)
        + "\n"
    )
    sys.exit(1)


def load_journals(excel_path: str) -> list[dict]:
    """Read the ABS Excel file and return a list of journal dicts."""
    wb = openpyxl.load_workbook(excel_path, data_only=True)
    ws = wb[SHEET_NAME]

    journals = []
    for row in ws.iter_rows(min_row=DATA_START_ROW, values_only=True):
        if row is None:
            continue
        # Columns: 0=ID, 1=Field, 2=Title, 3=AJG_2024
        field = str(row[1]).strip() if row[1] is not None else ""
        title_raw = str(row[2]).strip() if row[2] is not None else ""
        rating = str(row[3]).strip() if row[3] is not None else ""

        if not title_raw:
            continue
        if field in ("Field", ""):
            continue

        title = clean_journal_name(title_raw)

        journals.append(
            {
                "id": row[0],
                "field": field,
                "title": title,
                "rating": rating,
            }
        )

    wb.close()
    return journals


def filter_journals(
    journals: list[dict],
    fields: list[str] | None = None,
    ratings: list[str] | None = None,
) -> list[dict]:
    """Filter journals by field codes and rating levels.

    Args:
        journals: List of journal dicts.
        fields: ABS field codes (case-insensitive match). None or ["ALL"] means no filtering.
        ratings: Rating levels ("1","2","3","4","4*"). None means no filtering.

    Returns:
        Filtered list sorted by rating (4* first) then alphabetically by title.
    """
    result = []

    for j in journals:
        # Field filter
        if fields and "ALL" not in [f.upper() for f in fields]:
            match = False
            for f in fields:
                if j["field"].upper() == f.upper():
                    match = True
                    break
            if not match:
                continue

        # Rating filter
        if ratings:
            if j["rating"] not in ratings:
                continue

        result.append(j)

    # Sort: by rating (4* > 4 > 3 > 2 > 1), then alphabetically by title
    result.sort(
        key=lambda j: (
            RATING_ORDER.get(j["rating"], 99),
            j["title"].lower(),
        )
    )
    return result


def format_output(journals: list[dict], fmt: str) -> str:
    """Format filtered journals into the requested output format.

    Args:
        journals: Filtered journal list.
        fmt: One of "so", "ts", "list", "count", "csv".

    Returns:
        Formatted string. For "so" and "ts", the result can be very long.
    """
    if fmt == "count":
        return str(len(journals))

    if fmt == "list":
        return "\n".join(j["title"] for j in journals)

    if fmt == "csv":
        lines = ["ID,Field,Title,AJG_2024"]
        for j in journals:
            lines.append(f'{j["id"]},{j["field"]},"{j["title"]}",{j["rating"]}')
        return "\n".join(lines)

    if fmt in ("so", "ts"):
        prefix = "SO" if fmt == "so" else "TS"
        if not journals:
            return f'{prefix}=("")'
        names = [j["title"] for j in journals]
        # Escape any embedded double quotes
        escaped = [n.replace('"', "'") for n in names]
        quoted = [f'"{n}"' for n in escaped]
        clause = f'{prefix}=(' + " OR ".join(quoted) + ")"

        if len(clause) > 6000:
            sys.stderr.write(
                f"Warning: {prefix}= clause is {len(clause)} characters. "
                "WoS has an ~8000 character query limit. "
                "Consider splitting into multiple queries.\n"
            )
        return clause

    raise ValueError(f"Unknown format: {fmt}")


def list_fields(journals: list[dict]) -> str:
    """Return a formatted list of all unique field codes."""
    fields = sorted(set(j["field"] for j in journals), key=str.lower)
    counts = {}
    for j in journals:
        counts[j["field"]] = counts.get(j["field"], 0) + 1

    lines = [f"{'Field Code':<50} {'Journals':>8}", "-" * 60]
    for f in fields:
        lines.append(f"  {f:<48} {counts[f]:>8}")
    return "\n".join(lines)


def list_ratings() -> str:
    """Return formatted list of available ratings."""
    return "\n".join(
        [
            "Available ratings (ABS AJG 2024):",
            "  4*  - Journal of Distinction (highest)",
            "  4   - Top-tier journal",
            "  3   - High-quality journal",
            "  2   - Well-regarded journal",
            "  1   - Recognised journal",
        ]
    )


def main():
    parser = argparse.ArgumentParser(
        description="Query ABS Academic Journal Guide 2024 for WoS search queries."
    )
    parser.add_argument(
        "--fields",
        action="append",
        nargs="+",
        default=None,
        help="ABS field codes to include. Use ALL for all fields. "
        "Can be used multiple times: --fields 'INFO MAN' --fields MKT "
        "or with multiple codes: --fields 'INFO MAN' MKT",
    )
    parser.add_argument(
        "--ratings",
        action="append",
        nargs="+",
        default=None,
        help="Rating levels to include (1, 2, 3, 4, 4*). "
        "Can be used multiple times: --ratings 3 4 --ratings '4*'",
    )
    parser.add_argument(
        "--format",
        choices=["so", "ts", "list", "count", "csv"],
        default="so",
        help="Output format (default: so). "
        "so=WoS SO=() query, ts=WoS TS=() query, "
        "list=one journal per line, count=integer count, csv=CSV data",
    )
    parser.add_argument(
        "--list-fields",
        action="store_true",
        help="List all 22 ABS field codes with journal counts and exit.",
    )
    parser.add_argument(
        "--list-ratings",
        action="store_true",
        help="List available rating levels and exit.",
    )
    parser.add_argument(
        "--excel-path",
        default=None,
        help="Path to ABS2024.xlsx (default: auto-detect).",
    )

    args = parser.parse_args()

    # Resolve excel path
    if args.excel_path:
        excel_path = args.excel_path
        if not os.path.isfile(excel_path):
            sys.stderr.write(f"File not found: {excel_path}\n")
            sys.exit(1)
    else:
        excel_path = find_excel_path(os.path.dirname(os.path.abspath(__file__)))

    # Load data
    journals = load_journals(excel_path)

    # Handle list commands
    if args.list_fields:
        print(list_fields(journals))
        return
    if args.list_ratings:
        print(list_ratings())
        return

    # Flatten nested lists from action="append" (e.g., [["INFO MAN"], ["MKT"]] -> ["INFO MAN", "MKT"])
    if args.fields is not None:
        fields = [f for sublist in args.fields for f in sublist]
    else:
        fields = None

    if args.ratings is not None:
        ratings = [r for sublist in args.ratings for r in sublist]
    else:
        ratings = None

    # Filter
    result = filter_journals(journals, fields, ratings)

    # Output
    print(format_output(result, args.format))

    # Informational summary to stderr
    if args.format in ("so", "ts", "csv"):
        field_summary = ", ".join(fields) if fields else "ALL"
        rating_summary = ", ".join(ratings) if ratings else "ALL"
        sys.stderr.write(
            f"[{len(result)} journals matched: fields={field_summary}, "
            f"ratings={rating_summary}]\n"
        )


if __name__ == "__main__":
    main()
