#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Centralized logging configuration for the Code Processor application.
"""

import logging

def setup_logger():
    """
    Set up and configure the application logger.
    
    Returns:
        The configured logger instance
    """
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("code_processor.log"),
            logging.StreamHandler()
        ]
    )
    
    return logging.getLogger(__name__)

# Create a root logger that can be imported by other modules
logger = setup_logger()

def get_logger(name):
    """
    Get a logger for a specific module.
    
    Args:
        name: The name of the module (typically __name__)
        
    Returns:
        A logger instance for the module
    """
    return logging.getLogger(name)
