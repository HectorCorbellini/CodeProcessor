#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Helper functions for the Code Processor application.
"""

import os
from typing import Optional, Union
import webbrowser
import pyperclip
from tkinter import messagebox, filedialog
import customtkinter as ctk
from constants import SUPPORTED_FILE_TYPES
from texts import TEXTS
from logger import get_logger
from error_handler import with_error_handling

# Get module logger
logger = get_logger(__name__)

@with_error_handling("opening_url", return_on_error=False)
def open_url(url: str, platform_name: Optional[str] = None) -> bool:
    """
    Open a URL in the default web browser.
    
    Args:
        url: The URL to open
        platform_name: Optional name of the platform for error messages
    
    Returns:
        bool: True if successful, False otherwise
    """
    logger.info(f"Opening URL: {url}")
    webbrowser.open(url)
    return True

@with_error_handling("clipboard", return_on_error=False)
def copy_to_clipboard(text: str) -> bool:
    """
    Copy text to the clipboard.
    
    Args:
        text: The text to copy
    
    Returns:
        bool: True if successful, False otherwise
    """
    logger.info("Copying content to clipboard")
    pyperclip.copy(text)
    return True

@with_error_handling("save_file", return_on_error=False)
def save_to_file(content: str, default_filename: str = "processed_code.txt") -> bool:
    """
    Save content to a text file.
    
    Args:
        content: The content to save
        default_filename: Default filename to suggest
    
    Returns:
        bool: True if successful, False otherwise
    """
    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
        initialfile=default_filename
    )
    if file_path:
        logger.info(f"Saving content to file: {file_path}")
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(content)
        return True
    logger.info("File save cancelled by user")
    return False

def get_file_language(filename: str) -> str:
    """
    Get the programming language for a file based on its extension.
    
    Args:
        filename: The name of the file
        
    Returns:
        str: The language name or "Plain Text" if not recognized
    """
    _, ext = os.path.splitext(filename.lower())
    language = SUPPORTED_FILE_TYPES.get(ext, "Plain Text")
    logger.debug(f"File: {filename}, Language: {language}")
    return language

def change_appearance_mode(new_mode: str) -> None:
    """
    Change the appearance mode of the application.
    
    Args:
        new_mode: The new appearance mode ("Light", "Dark", or "System")
    """
    logger.info(f"Changing appearance mode to: {new_mode}")
    ctk.set_appearance_mode(new_mode)

def select_directory() -> Optional[str]:
    """
    Open a directory selection dialog.
    
    Returns:
        str: Selected directory path or None if canceled
    """
    directory = filedialog.askdirectory(title="Select Directory")
    if directory:
        logger.info(f"Selected directory: {directory}")
    else:
        logger.info("Directory selection cancelled by user")
    return directory
