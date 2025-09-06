"""Generate a fabrication PDF from the KiCad project files. Note that this requires kicad-python, which requires KiCad
to be open with the current board file.

Copyright (c) 2025 Isaac Rex
SPDX-License-Identifier: MIT
"""
import os
from pathlib import Path
from kipy import KiCad
from kipy.board import Board, BoardStackupLayer
from kikit_tools.utils import find_kicad_python, get_kikit_tools_path, get_open_board_path
from kipy.errors import ApiError
import subprocess

# ${KICAD9_3RD_PARTY}/plugins/com_gitlab_dennevi_Board2Pdf/board2pdf-cli.py --ini '${KIPRJMOD}/board2pdf_Fab_4L.config.ini' --ext _FAB '${PROJECTNAME}.kicad_pcb'

KICAD9_3RD_PARTY = Path(os.path.expandvars("${KICAD9_3RD_PARTY}"))
BOARD2PDF_PATH = KICAD9_3RD_PARTY/"plugins"/"com_gitlab_dennevi_Board2Pdf"/"board2pdf-cli.py"
FILE_SUFFIX_FAB = "_FAB"
CONFIG_FILE_FORMAT_STR = "board2pdf_Fab_{layer_count}L.config.ini" 
CONFIG_FILE_DIR = get_kikit_tools_path() / "releaser" / "configs" # Directory containing the config files

def get_copper_layer_count(board: Board) -> int:
    """Returns the number of copper layers in the board.
    TODO: Written for kipy 0.4.0, 0.5.0 will add Board.get_copper_layer_count. Replace when updated.    

    Args:
        board (Board): KiCad Board object

    Returns:
        int: Number of copper layers in the board
    """
    layers: list[BoardStackupLayer] = board.get_stackup().layers

    return len([l for l in layers if l.user_name.endswith(".Cu")])

def _get_config_path() -> Path:
    kicad = KiCad()
    try:
        board = kicad.get_board()
    except (ApiError) as e:
        print(f"Error connecting to KiCad, is the board file open?")
        # Just quit for now
        exit(1)

    config_file_path = CONFIG_FILE_DIR / CONFIG_FILE_FORMAT_STR.format(layer_count=get_copper_layer_count(board))
    if not config_file_path.exists():
        raise FileNotFoundError(
            f"Could not find the config file for {get_copper_layer_count(board)} layers at {config_file_path}")
    return config_file_path

def generate_pdf(board_path: Path, config_path: Path, suffix: str = ""):
    """Generates a fabrication PDF from the KiCad board file.
    """
    python_kicad_path = find_kicad_python()
    if not python_kicad_path:
        raise RuntimeError("Could not find the KiCad bundled python executable.")

    # Spawn a subprocess and run the board2pdf script
    subprocess.run([python_kicad_path, BOARD2PDF_PATH,
                    "--ini", str(config_path),
                    "--ext", suffix,
                    str(board_path)],
                   check=True)
    
if __name__ == "__main__":
    config_file_path = _get_config_path()
    try:
        board_path = get_open_board_path()
    except (ApiError) as e:
        print(f"Error connecting to KiCad, is the board file open?")
        # Just quit for now
        exit(1)

    generate_pdf(board_path=board_path, config_path=config_file_path, suffix=FILE_SUFFIX_FAB)