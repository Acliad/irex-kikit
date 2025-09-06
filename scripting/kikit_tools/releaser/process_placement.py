"""Process a placement file exported from KiCAD to conform to JLC PCB requirements. It renames the headers to match 
the JLC expected format. 

NOTE: This can be depreciated once KiCAD updates its placement file export to customize the generated file.

Copyright (c) 2025 Isaac Rex
SPDX-License-Identifier: MIT
"""

import argparse
from pathlib import Path
from dataclasses import dataclass

FILE_NOT_FOUND_ERROR = 1

@dataclass
class Replacements:
    old: str
    new: str

header_replacements = [
    Replacements("Ref", "Designator"),
    Replacements("PosX", "\"Mid X\""),
    Replacements("PosY", "\"Mid Y\""),
    Replacements("Rot", "Rotation"),
    Replacements("Side", "Layer")
]


def process_placement_files(file_path: Path):
    print(file_path)
    files = list(file_path.parent.glob(file_path.name))
    if not files:
        print(f"Error: No file found for {file_path}")
        exit(FILE_NOT_FOUND_ERROR)
    
    for file_path in files:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            header = lines[0]
            for replacement in header_replacements:
                header = header.replace(replacement.old, replacement.new)
        # Rewrite the file
        lines[0] = header
        with open(file_path, 'w') as file:
            file.writelines(lines)
        print(f"Processed {file_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process a KiCAD placement file to conform to JLC PCB requirements.")
    parser.add_argument("path", type=Path, help="Path to the placement file(s) to process. Paths can be glob patterns.")
    
    args = parser.parse_args()
    process_placement_files(args.path)

    