#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UI component factory functions for the Code Processor application.
"""

from typing import Any, Callable, Dict, List, Optional
import customtkinter as ctk
from constants import DEFAULT_FONT_SIZE, DEFAULT_BUTTON_HEIGHT, DEFAULT_PADDING, TITLE_COLOR, TITLE_BG_COLOR
from logger import get_logger

# Get module logger
logger = get_logger(__name__)

def create_button(parent: Any, 
                 text: Optional[str] = None, 
                 command: Optional[Callable[[], None]] = None, 
                 font_size: Optional[int] = None, 
                 height: Optional[int] = None,
                 is_dropdown: bool = False,
                 is_textbox: bool = False,
                 **kwargs: Any) -> Any:
    """
    Create a button with standard styling.
    
    Args:
        parent: The parent widget
        text: Button text
        command: Button command callback
        font_size: Font size (defaults to DEFAULT_FONT_SIZE)
        height: Button height (defaults to DEFAULT_BUTTON_HEIGHT)
        is_dropdown: If True, creates a dropdown menu instead of a button
        is_textbox: If True, creates a textbox instead of a button
        **kwargs: Additional button configuration parameters
        
    Returns:
        The created widget (button, dropdown, or textbox)
    """
    # Handle special cases first
    if is_textbox:
        config = {
            'font': ctk.CTkFont(family="Consolas", size=font_size if font_size is not None else DEFAULT_FONT_SIZE),
            'wrap': "none",
        }
        
        # Add any additional kwargs
        config.update(kwargs)
        
        return ctk.CTkTextbox(parent, **config)
    
    if is_dropdown:
        config = {
            'font': ctk.CTkFont(size=font_size if font_size is not None else DEFAULT_FONT_SIZE),
        }
        
        if command is not None:
            config['command'] = command
            
        # Add any additional kwargs
        config.update(kwargs)
        
        return ctk.CTkOptionMenu(parent, **config)
    
    # Regular button
    config = {
        'font': ctk.CTkFont(size=font_size if font_size is not None else DEFAULT_FONT_SIZE),
        'height': height if height is not None else DEFAULT_BUTTON_HEIGHT,
    }
    
    if text is not None:
        config['text'] = text
    
    if command is not None:
        config['command'] = command
    
    # Add any additional kwargs
    config.update(kwargs)
    
    return ctk.CTkButton(parent, **config)

def create_label(parent: Any,
                text: Optional[str] = None,
                is_title: bool = False,
                font_size: Optional[int] = None,
                **kwargs: Any) -> ctk.CTkLabel:
    """
    Create a label with standard styling.
    
    Args:
        parent: The parent widget
        text: Label text
        is_title: Whether this is a title label (with special styling)
        font_size: Font size (defaults to DEFAULT_FONT_SIZE)
        **kwargs: Additional label configuration parameters
        
    Returns:
        The created label
    """
    config = {
        'font': ctk.CTkFont(
            size=font_size if font_size is not None else DEFAULT_FONT_SIZE,
            weight="bold" if is_title else "normal"
        ),
        'anchor': "w",
    }
    
    if is_title:
        config.update({
            'text_color': TITLE_COLOR,
            'fg_color': TITLE_BG_COLOR,
            'corner_radius': 6
        })
    
    if text is not None:
        config['text'] = text
        
    # Add any additional kwargs
    config.update(kwargs)
    
    return ctk.CTkLabel(parent, **config)

def create_frame(parent: Any,
                with_padding: bool = True,
                **kwargs: Any) -> ctk.CTkFrame:
    """
    Create a frame with standard styling.
    
    Args:
        parent: The parent widget
        with_padding: Whether to add default padding
        **kwargs: Additional frame configuration parameters
        
    Returns:
        The created frame
    """
    frame = ctk.CTkFrame(parent, **kwargs)
    
    if with_padding:
        frame.pack(fill="both", expand=True, padx=DEFAULT_PADDING, pady=DEFAULT_PADDING)
    else:
        frame.pack(fill="both", expand=True)
        
    return frame
