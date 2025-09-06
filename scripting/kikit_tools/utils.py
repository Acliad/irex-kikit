"""A collection of utility functions for kikit scripts.

Copyright (c) 2025 Isaac Rex
SPDX-License-Identifier: MIT
"""

import os
import sys
import platform
import subprocess
from pathlib import Path
from kipy import KiCad
from kipy.proto.common.types import DocumentType
from kipy.errors import ConnectionError, ApiError


def _find_kicad_python_windows() -> str | None:
    """
    Find the KiCad Python executable path on Windows.
    This function searches common installation paths and checks the Windows Registry.
    Returns:
        str: Path to KiCad Python executable or None if not found
    """
    # Common KiCad installation locations on Windows
    kicad_install_paths = [
        Path("C:/Program Files/KiCad"),
        Path("C:/Program Files (x86)/KiCad"),
        # Add custom installation location if provided in environment variable
        Path(os.environ.get("KICAD_PATH", "C:/KiCad"))
    ]
    
    # Find latest KiCad version (if multiple exist)
    for base_path in kicad_install_paths:
        if not base_path.exists():
            continue
            
        # Try to find the version-specific directories (like 7.0)
        versions = []
        try:
            # Check for version subdirectories
            for item in base_path.iterdir():
                if item.is_dir() and item.name[0].isdigit():
                    versions.append(item)
        except (PermissionError, FileNotFoundError):
            continue
            
        # If version subdirectories found, sort numerically by version
        if versions:
            # Sort version directories numerically instead of lexicographically
            def version_key(path):
                # Extract version components and convert to float for proper numeric comparison
                try:
                    # Handle formats like "7.0" or "10.0"
                    return float(path.name.split()[0])
                except (ValueError, IndexError):
                    # Fallback in case of non-standard naming
                    return 0
            
            versions.sort(key=version_key, reverse=True)
            
            for version_path in versions:
                # Look for Python in the bin directory
                python_path = version_path / "bin" / "python.exe"
                if python_path.exists():
                    return str(python_path)
                    
                # Check alternative path structure
                python_path = version_path / "python" / "python.exe"  
                if python_path.exists():
                    return str(python_path)
        
        # If no version directories or python not found, try default structure
        python_path = base_path / "bin" / "python.exe"
        if python_path.exists():
            return str(python_path)
            
        # Try another common structure
        python_path = base_path / "python" / "python.exe"
        if python_path.exists():
            return str(python_path)
            
    # If we get here, we didn't find KiCad's Python in common locations
    # Try checking Windows Registry
    try:
        import winreg
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\KiCad") as key:
            install_dir, _ = winreg.QueryValueEx(key, "InstallDir")
            if install_dir:
                python_path = Path(install_dir) / "bin" / "python.exe"
                if python_path.exists():
                    return str(python_path)
    except (ImportError, FileNotFoundError, PermissionError):
        pass
        
    print("KiCad Python not found on Windows")
    return None

def _find_kicad_python_macos() -> str | None:
    """
    Find the KiCad Python executable path on macOS.
    This function searches common installation paths.
    Returns:
        str: Path to KiCad Python executable or None if not found
    """
    # Common KiCad installation location on macOS
    kicad_app_paths = [
        Path("/Applications/KiCad/KiCad.app"),
        Path("/Applications/KiCad.app")
    ]
    
    # Find the KiCad.app location
    kicad_app_path = None
    for path in kicad_app_paths:
        if path.exists():
            kicad_app_path = path
            break
    
    if kicad_app_path:
        # First check the standard Python location
        python_path = kicad_app_path / "Contents/Frameworks/Python.framework/Versions/Current/bin/python3"
        
        # Resolve symlink if it exists
        if python_path.exists():
            python_path = python_path.resolve()
            return str(python_path)
            
        # If not found, try the direct Python executable
        python_path = kicad_app_path / "Contents/Frameworks/Python.framework/Versions/Current/Python"
        
        # Resolve symlink if it exists
        if python_path.exists():
            python_path = python_path.resolve()
            return str(python_path)
            
        # As a last resort, search in all of Frameworks
        frameworks_dir = kicad_app_path / "Contents/Frameworks"
        for root, dirs, files in os.walk(frameworks_dir):
            root_path = Path(root)
            for file in files:
                if file == "python3" or file == "Python":
                    python_path = root_path / file
                    if python_path.is_file() and os.access(python_path, os.X_OK):  # Check if executable
                        # Resolve symlink if it exists
                        python_path = python_path.resolve()
                        return str(python_path)
    
    print("KiCad Python not found on macOS")
    return None

def find_kicad_python() -> str | None:
    """
    Find the KiCad Python executable path based on the current platform.
    Currently supports:
        - macOS: Automatically locates KiCad's Python in standard installation locations
        - Windows: Not yet tested
    
    Returns:
        str: Path to KiCad Python executable or None if not found
    """
    system = platform.system()
    
    if system == "Windows":
        return _find_kicad_python_windows()
    
    elif system == "Darwin":  # macOS
        return _find_kicad_python_macos()
    
    else:
        print(f"Unsupported operating system: {system}")
        return None

def get_kikit_tools_path() -> Path:
    """Get the path to the KiKit tools directory.

    Returns:
        Path: Path to the KiKit tools directory
    """
    return Path(__file__).resolve().parent

def get_open_board_path() -> Path:
    """Get the path to the currently open KiCad board file. Requires the board to be open in KiCad.

    Returns:
        Path | None: Path to the open board file or None if not found
    Raises:
        ConnectionError: If unable to connect to KiCad instance
        ApiError: If there is an error retrieving the board from KiCad (must be open!)
    """
    kicad = KiCad()
    pcb_doc = kicad.get_open_documents(DocumentType.DOCTYPE_PCB)
    return Path(pcb_doc[0].project.path) / pcb_doc[0].board_filename
