#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File processing functions for the Code Processor application.
"""

import os
from typing import List, Tuple, Optional
from pathlib import Path
from constants import SUPPORTED_FILE_TYPES
from helpers import get_file_language
from texts import TEXTS
from logger import get_logger
from file_utils import (
    normalize_path, get_relative_path, is_supported_file,
    list_files_in_directory, read_file_with_fallback
)
from error_handler import with_error_handling

# Get module logger
logger = get_logger(__name__)

@with_error_handling("processing_directory", return_on_error=[])
def process_directory(directory: str) -> List[Tuple[str, str]]:
    """
    Process a directory to find and list code files.
    
    Args:
        directory: The directory path to process
        
    Returns:
        list: List of tuples (file_path, relative_path)
    """
    logger.info(f"Processing directory: {directory}")
    
    # Normalize directory path
    directory = normalize_path(directory)
    
    # Walk through directory and find supported files
    files = []
    try:
        for root, _, filenames in os.walk(directory):
            for filename in filenames:
                file_path = os.path.join(root, filename)
                _, ext = os.path.splitext(filename.lower())
                
                # Check if file type is supported
                if ext in SUPPORTED_FILE_TYPES:
                    # Use relative path from the selected directory
                    rel_path = os.path.relpath(file_path, directory)
                    files.append((file_path, rel_path))
                    logger.debug(f"Added file: {rel_path}")
        
        # Sort files by relative path
        files.sort(key=lambda x: x[1])
        logger.info(f"Found {len(files)} supported files")
    except Exception as e:
        logger.error(f"Error processing directory: {str(e)}", exc_info=True)
    
    return files

@with_error_handling("formatting_code", return_on_error="")
def format_files_for_ai(files: List[Tuple[str, str]]) -> str:
    """
    Format a list of files for AI platforms.
    
    Args:
        files: List of tuples (file_path, relative_path)
        
    Returns:
        str: Formatted content with file paths, language info, and code
    """
    if not files:
        logger.warning("No files to format")
        return ""
    
    logger.info(f"Formatting {len(files)} files for AI platform")
    
    formatted_content = ""
    
    for file_path, rel_path in files:
        # Get language for syntax highlighting
        language = get_file_language(file_path)
        
        # Add file header
        formatted_content += TEXTS["file_path"].format(path=rel_path) + "\n"
        formatted_content += TEXTS["file_language"].format(language=language) + "\n"
        formatted_content += "```" + language.lower() + "\n"
        
        # Read and add file content
        content, error = read_file_with_fallback(file_path)
        if error:
            logger.error(f"Error reading file {rel_path}: {error}")
            formatted_content += TEXTS["file_error_read"].format(error=error) + "\n"
        else:
            formatted_content += content
            logger.debug(f"Successfully read file: {rel_path}")
        
        # Close code block and add separator
        formatted_content += "\n```\n\n"
    
    return formatted_content

@with_error_handling("parsing_dropped_files", return_on_error=[])
def parse_dropped_files(drop_data: str) -> List[str]:
    """
    Parse dropped files/directories from drag and drop event.
    
    Args:
        drop_data: The data from the drop event
        
    Returns:
        list: List of file/directory paths
    """
    # Remove curly braces and handle file paths
    paths = []
    
    logger.info("Parsing dropped files data")
    # Handle different formats of drop data
    if drop_data.startswith("{") and drop_data.endswith("}"):
        # Windows format: {path1} {path2}
        logger.debug("Detected Windows-style drop format")
        data = drop_data.strip("{}")
        paths = [p.strip("{}") for p in data.split("} {")]
    else:
        # Unix format: path1 path2
        logger.debug("Detected Unix-style drop format")
        paths = drop_data.split()
    
    # Clean up paths
    paths = [normalize_path(p.strip()) for p in paths if p.strip()]
    logger.info(f"Parsed {len(paths)} paths from drop data")
    
    return paths
