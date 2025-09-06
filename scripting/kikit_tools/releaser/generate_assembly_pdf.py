"""Generate an assembly PDF from the KiCad project files. Note that this requires kicad-python, which requires KiCad
to be open with the current board file.

Copyright (c) 2025 Isaac Rex
SPDX-License-Identifier: MIT
"""

from kikit_tools.releaser.generate_fab_pdf import generate_pdf, CONFIG_FILE_DIR
from kikit_tools.utils import get_open_board_path
from pathlib import Path

FILE_SUFFIX_ASY = "_ASY"
CONFIG_FILE_FORMAT_STR = "board2pdf_Asy.config.ini" 

if __name__ == "__main__":
    config_file_path = CONFIG_FILE_DIR / CONFIG_FILE_FORMAT_STR
    board_path = get_open_board_path()
    generate_pdf(board_path=board_path, config_path=config_file_path, suffix=FILE_SUFFIX_ASY)