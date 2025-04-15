#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File utility functions for the Code Processor application.
"""

import os
from pathlib import Path
from typing import List, Optional, Tuple
from constants import SUPPORTED_FILE_TYPES
from logger import get_logger

# Get module logger
logger = get_logger(__name__)

def normalize_path(path: str) -> str:
    """
    Normalize a file path to use consistent separators and resolve relative paths.
    
    Args:
        path: The path to normalize
        
    Returns:
        The normalized path
    """
    return os.path.normpath(path)

def get_relative_path(path: str, base_dir: str) -> str:
    """
    Get the relative path from a base directory.
    
    Args:
        path: The absolute path
        base_dir: The base directory
        
    Returns:
        The relative path
    """
    return os.path.relpath(path, base_dir)

def get_file_extension(filename: str) -> str:
    """
    Get the file extension from a filename.
    
    Args:
        filename: The filename
        
    Returns:
        The file extension without the dot
    """
    return os.path.splitext(filename)[1][1:].lower()

def is_supported_file(filename: str) -> bool:
    """
    Check if a file is supported based on its extension.
    
    Args:
        filename: The filename to check
        
    Returns:
        True if the file is supported, False otherwise
    """
    ext = get_file_extension(filename)
    return ext in SUPPORTED_FILE_TYPES

def list_files_in_directory(directory: str, recursive: bool = True) -> List[str]:
    """
    List all supported files in a directory.
    
    Args:
        directory: The directory to list files from
        recursive: Whether to search recursively
        
    Returns:
        A list of file paths
    """
    files = []
    directory = normalize_path(directory)
    
    logger.info(f"Listing files in directory: {directory}")
    
    if recursive:
        for root, _, filenames in os.walk(directory):
            for filename in filenames:
                if is_supported_file(filename):
                    files.append(os.path.relpath(os.path.join(root, filename), directory))
    else:
        for item in os.listdir(directory):
            full_path = os.path.join(directory, item)
            if os.path.isfile(full_path) and is_supported_file(item):
                files.append(os.path.relpath(full_path, directory))
    
    logger.info(f"Found {len(files)} supported files")
    return files

def read_file_with_fallback(file_path: str) -> Tuple[str, Optional[str]]:
    """
    Read a file with encoding fallback.
    
    Args:
        file_path: The path to the file
        
    Returns:
        A tuple of (file_content, error_message)
    """
    encodings = ['utf-8', 'latin-1', 'cp1252']
    
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as file:
                content = file.read()
            return content, None
        except UnicodeDecodeError:
            continue
        except Exception as e:
            error_msg = f"Error reading file {file_path}: {str(e)}"
            logger.error(error_msg, exc_info=True)
            return "", error_msg
    
    error_msg = f"Could not decode file {file_path} with any of the attempted encodings"
    logger.error(error_msg)
    return "", error_msg
