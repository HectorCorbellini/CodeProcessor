#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Error handling utilities for the Code Processor application.
"""

import functools
from tkinter import messagebox
from logger import get_logger
from texts import TEXTS

# Get module logger
logger = get_logger(__name__)

def with_error_handling(operation_name, show_dialog=True, return_on_error=False):
    """
    Decorator for standardized error handling.
    
    Args:
        operation_name: Name of the operation (used for logging and error text key)
        show_dialog: Whether to show an error dialog to the user
        return_on_error: Value to return if an error occurs
        
    Returns:
        Decorated function with error handling
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                error_key = f"error_{operation_name}"
                error_msg = str(e)
                
                # Use text from TEXTS if available, otherwise use generic message
                if error_key in TEXTS:
                    formatted_error = TEXTS[error_key].format(error=error_msg)
                else:
                    formatted_error = f"Error in {operation_name}: {error_msg}"
                
                # Log the error
                logger.error(formatted_error, exc_info=True)
                
                # Show error dialog if requested
                if show_dialog:
                    messagebox.showerror("Error", formatted_error)
                
                return return_on_error
        return wrapper
    return decorator
