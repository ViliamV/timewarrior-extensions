#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Percentage - Timewarrior report with %
Author: Viliam Valent

Usage:
timew percentage

OR

timew percentage :lastweek/:week/:day
"""

import json
import sys

from collections import defaultdict
from datetime import datetime
from itertools import chain
from typing import DefaultDict, Iterable, TextIO, Tuple


ParsedData = DefaultDict[str, int]
Row = Tuple[str, ...]
Lengths = Tuple[int, ...]


TAG_HEADER = "Tag"
DURATION_HEADER = "Duration"
PERCENTAGE_HEADER = "Portion"
SEPARATOR_CHAR = "-"
COLUMN_SPACING = "  "
SORTED = True
REVERSE = True
SORT_BY = 1  # valid values: 0, 1, or 2


def format_seconds(seconds: int) -> str:
    hours, rest = divmod(seconds, 3600)
    return f"{hours}:{(rest // 60):02d}"


def format_percentage(value: float) -> str:
    return f"{value:6,.1%}"


def row_str(row: Row, lengths: Lengths) -> str:
    return COLUMN_SPACING.join(f"{value:{length}}" for value, length in zip(row, lengths))


def separator_str(lengths: Lengths) -> str:
    return row_str(tuple(SEPARATOR_CHAR * length for length in lengths), lengths)


def ghetto_tabulate(totals: ParsedData) -> None:
    if not totals:
        error_and_exit("No data in selected interval.")
    total = sum(x for x in totals.values())
    header = (TAG_HEADER, DURATION_HEADER, PERCENTAGE_HEADER)
    items = (
        totals.items()
        if not SORTED
        else sorted(totals.items(), reverse=REVERSE, key=lambda row: row[SORT_BY])
    )
    body = [(tag, format_seconds(seconds), format_percentage(seconds / total)) for tag, seconds in items]
    footer = ("Total", format_seconds(total), format_percentage(1))
    lengths = tuple(max(len(row[i]) for row in chain([header, footer], body)) for i in range(3))
    output = "\n".join(
        [row_str(header, lengths), separator_str(lengths)]
        + [row_str(row, lengths) for row in body]
        + [separator_str(lengths), row_str(footer, lengths)]
    )
    print(output)


def error_and_exit(error: str) -> None:
    print(error)
    sys.exit(1)


def parse(input_stream: TextIO) -> ParsedData:
    DATEFORMAT = "%Y%m%dT%H%M%SZ"
    header = True
    config = {}
    body = ""
    for line in input_stream:
        if header:
            if line == "\n":
                header = False
                continue
            try:
                key, value = line.strip().split(": ", 1)
                config[key] = value
            except ValueError:
                continue
        else:
            body += line
    if "temp.report.tags" in config:
        error_and_exit("This report only works without tags.")
    totals: ParsedData = defaultdict(lambda: 0)
    tracked = json.loads(body)
    for session in tracked:
        start = datetime.strptime(session["start"], DATEFORMAT)
        if "end" in session:
            end = datetime.strptime(session["end"], DATEFORMAT)
        else:
            end = datetime.utcnow()
        duration = int((end - start).total_seconds())
        if not session.get("tags"):
            totals["untagged"] += duration
        else:
            if len(session["tags"]) > 1:
                error_and_exit("This report can only report one tag per session.")
            totals[session["tags"][0]] += duration
    return totals


if __name__ == "__main__":
    ghetto_tabulate(parse(sys.stdin))
