#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Centralized configuration for the Code Processor application.
"""

import os
from typing import Dict, Any
from logger import get_logger

# Get module logger
logger = get_logger(__name__)

class AppConfig:
    """Application configuration manager."""
    
    # Default configuration
    _config = {
        "app": {
            "name": "Code Processor",
            "version": "1.0.0",
            "language": "en",  # Default language
        },
        "ui": {
            "appearance_mode": "System",  # Light, Dark, or System
            "default_theme": "blue",
            "font_size": 15,
            "button_height": 30,
            "padding": 5,
            "colors": {
                "title": "#5D0024",
                "title_bg": "#E6D0D6",
                "button_fg": "#3a7ebf",
                "button_hover": "#2a6eaf",
            }
        },
        "files": {
            "default_save_filename": "processed_code.txt",
            "recursive_search": True,
        },
        "paths": {
            "log_file": "code_processor.log",
            "config_file": "config.json",
        }
    }
    
    @classmethod
    def get(cls, section: str, key: str, default: Any = None) -> Any:
        """
        Get a configuration value.
        
        Args:
            section: Configuration section
            key: Configuration key
            default: Default value if not found
            
        Returns:
            The configuration value or default
        """
        try:
            return cls._config[section][key]
        except KeyError:
            logger.warning(f"Configuration {section}.{key} not found, using default: {default}")
            return default
    
    @classmethod
    def set(cls, section: str, key: str, value: Any) -> None:
        """
        Set a configuration value.
        
        Args:
            section: Configuration section
            key: Configuration key
            value: Value to set
        """
        if section not in cls._config:
            cls._config[section] = {}
        
        cls._config[section][key] = value
        logger.info(f"Configuration {section}.{key} set to {value}")
    
    @classmethod
    def get_section(cls, section: str) -> Dict[str, Any]:
        """
        Get an entire configuration section.
        
        Args:
            section: Configuration section
            
        Returns:
            The configuration section or empty dict if not found
        """
        return cls._config.get(section, {})
    
    @classmethod
    def set_language(cls, language: str) -> None:
        """
        Set the application language.
        
        Args:
            language: Language code (e.g., 'en', 'es')
        """
        cls.set("app", "language", language)
        logger.info(f"Application language set to {language}")
    
    @classmethod
    def get_language(cls) -> str:
        """
        Get the current application language.
        
        Returns:
            The current language code
        """
        return cls.get("app", "language", "en")
    
    @classmethod
    def set_appearance_mode(cls, mode: str) -> None:
        """
        Set the UI appearance mode.
        
        Args:
            mode: Appearance mode (Light, Dark, or System)
        """
        cls.set("ui", "appearance_mode", mode)
        logger.info(f"Appearance mode set to {mode}")
    
    @classmethod
    def get_appearance_mode(cls) -> str:
        """
        Get the current UI appearance mode.
        
        Returns:
            The current appearance mode
        """
        return cls.get("ui", "appearance_mode", "System")
