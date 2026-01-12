"""
System dependency checker for Voice Cloning Engine.

This module verifies that required system dependencies (eSpeak-NG)
are properly installed and configured.
"""
import os
import sys
import shutil
from config import ESPEAK_POSSIBLE_PATHS, ESPEAK_DLL_NAMES, ESPEAK_COMMANDS


def check_espeak_installed():
    """
    Check if eSpeak-NG is installed and configure environment variables.
    
    This function searches for eSpeak-NG in common installation directories,
    locates the shared library (DLL), and sets the PHONEMIZER_ESPEAK_LIBRARY
    environment variable.
    
    Returns:
        bool: True if eSpeak-NG is found and configured, False otherwise.
    """
    found_exe_in_path = False
    
    # Check if eSpeak executables are in PATH
    for cmd in ESPEAK_COMMANDS:
        exe_path = shutil.which(cmd)
        if exe_path:
            print(f"Found {cmd} in PATH at: {exe_path}")
            found_exe_in_path = True
    
    # Search for eSpeak DLL in executable directory
    for exe_cmd in ESPEAK_COMMANDS:
        exe_path = shutil.which(exe_cmd)
        if exe_path:
            exe_dir = os.path.dirname(exe_path)
            for dll in ESPEAK_DLL_NAMES:
                candidate = os.path.join(exe_dir, dll)
                if os.path.exists(candidate):
                    os.environ['PHONEMIZER_ESPEAK_LIBRARY'] = candidate
                    print(f"Found espeak shared library at: {candidate}")
                    return True
    
    # Search in common installation directories
    for path in ESPEAK_POSSIBLE_PATHS:
        if os.path.exists(path):
            # Search for DLL files
            for root, _, files in os.walk(path):
                for dll in ESPEAK_DLL_NAMES:
                    candidate = os.path.join(root, dll)
                    if os.path.exists(candidate):
                        os.environ['PHONEMIZER_ESPEAK_LIBRARY'] = candidate
                        os.environ['PATH'] = f"{path};{os.environ['PATH']}"
                        print(f"Found espeak shared library at: {candidate}")
                        return True
            
            # Check for executable
            bin_path = os.path.join(path, 'espeak-ng.exe')
            if os.path.exists(bin_path):
                print(f"Found espeak-ng executable at: {bin_path}")
                print("Adding to PATH...")
                os.environ['PATH'] = f"{path};{os.environ['PATH']}"
                break
    
    # If we found the executable but not the DLL, still return True
    if found_exe_in_path:
        return True
    
    # eSpeak not found
    print("\nError: espeak-ng not found!")
    print("Install from https://github.com/espeak-ng/espeak-ng/releases")
    return False


def verify_system_requirements():
    """
    Verify all system requirements are met.
    
    Returns:
        bool: True if all requirements are met, False otherwise.
    """
    if not check_espeak_installed():
        print("\nSystem requirements not met. Exiting...")
        return False
    
    print("✓ All system requirements verified")
    return True
