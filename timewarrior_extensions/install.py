#!/usr/bin/env python
# -*- coding: utf-8 -*-
from functools import partial
from os import symlink
from pathlib import Path
from sys import exit
from typing import Optional


PARENT = Path(__file__).parent
MAX_TRIES = 3


def _timewarrior_location() -> Optional[Path]:
    timew_dir = Path.home() / ".timewarrior"
    for i in range(MAX_TRIES):
        if timew_dir.is_dir():
            return timew_dir / "extensions/"
        print(f"Directory {timew_dir} not found.")
        timew_dir = Path(input("Full path to timewarrior directory: "))
    print("Maximum number of tries reached.")
    return None


def _install(file_name: str) -> None:
    src = PARENT / file_name
    if not src.is_file():
        raise Exception("Trying to install nonexisting file")
    if (timew_dir := _timewarrior_location()) is not None:
        dest = timew_dir / file_name
        try:
            symlink(str(src.resolve()), str(dest.resolve()))
            print(f"Successfully installed extension {file_name}")
        except FileExistsError:
            print(f"File {file_name} already exits in {dest}.")
    else:
        exit(1)


install_percentage = partial(_install, "percentage.py")
