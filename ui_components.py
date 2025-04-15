#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UI components for the Code Processor application.
"""

import tkinter as tk
from typing import Any, Callable, Dict, List, Optional, Tuple, Union, TypeVar, cast

import customtkinter as ctk
from tkinterdnd2 import DND_FILES, TkinterDnD

from constants import (
    AI_PLATFORMS, DEFAULT_BUTTON_HEIGHT, DEFAULT_FONT_SIZE, 
    DEFAULT_PADDING, TITLE_BG_COLOR, TITLE_COLOR
)
from helpers import open_url
from texts import TEXTS
from ui_factory import create_button, create_label, create_frame
from logger import get_logger

# Get module logger
logger = get_logger(__name__)

# Type aliases for better type hinting
WidgetEvent = TypeVar('WidgetEvent', bound=tk.Event)
ButtonCallback = Callable[[], None]

def create_right_sidebar(parent: ctk.CTk, app_instance: Any) -> Tuple[ctk.CTkFrame, List[ctk.CTkButton]]:
    """
    Create the right sidebar with AI platform buttons.
    
    Args:
        parent: The parent tkinter window
        app_instance: The main application instance for callbacks
    
    Returns:
        Tuple containing:
            - frame: The sidebar frame
            - buttons: List of platform buttons
    """
    # Create right sidebar frame
    sidebar = create_frame(parent, width=140, corner_radius=0)
    sidebar.grid(row=0, column=1, sticky="nsew")
    
    # Add title for AI platforms
    title = create_label(
        sidebar, 
        text=TEXTS["title_ai_platforms"], 
        is_title=True,
        font_size=16
    )
    title.grid(row=0, column=0, padx=DEFAULT_PADDING, pady=(10, 5), sticky="ew")
    
    # Add buttons for each AI platform
    platforms_list = list(AI_PLATFORMS.items())
    platform_buttons = []
    
    for i, (platform_name, (url, icon)) in enumerate(platforms_list):
        platform_button = create_button(
            sidebar, 
            text=f"{icon} {platform_name}", 
            command=lambda u=url: open_url(u)
        )
        platform_button.grid(row=i+1, column=0, padx=DEFAULT_PADDING, pady=5, sticky="ew")
        platform_buttons.append(platform_button)
    
    # Now configure the row weight after all buttons are placed
    # This ensures the empty space is at the bottom
    last_row = len(platforms_list)+1
    sidebar.grid_rowconfigure(last_row, weight=1)
    
    return sidebar, platform_buttons

def _create_platform_button(parent: ctk.CTkFrame, 
                           platform_name: str, 
                           platform_icon: str, 
                           row_index: int, 
                           callback: Callable[[str], Any]) -> ctk.CTkButton:
    """
    Create a button for an AI platform.
    
    Args:
        parent: The parent frame
        platform_name: Name of the AI platform
        platform_icon: Icon for the AI platform
        row_index: Row index for grid placement
        callback: Callback function for button click
        
    Returns:
        button: The created button
    """
    button = create_button(
        parent,
        text=f"{platform_icon} {platform_name}",
        command=lambda: callback(platform_name)
    )
    button.grid(row=row_index, column=0, padx=DEFAULT_PADDING, pady=5, sticky="ew")
    
    return button

def create_appearance_mode_section(parent: ctk.CTkFrame, 
                                  start_row: int, 
                                  callback: Callable[[str], None]) -> Tuple[ctk.CTkLabel, ctk.CTkOptionMenu]:
    """
    Create the appearance mode section in the sidebar.
    
    Args:
        parent: The parent frame
        start_row: The row to start placing the appearance mode controls
        callback: The callback function for appearance mode changes
    
    Returns:
        tuple: The appearance mode label and option menu
    """
    # Appearance mode label
    appearance_label = create_label(
        parent, 
        text=TEXTS["title_appearance"], 
        anchor="w",
        font_size=DEFAULT_FONT_SIZE,
        is_title=True
    )
    appearance_label.grid(row=start_row, column=0, padx=DEFAULT_PADDING, pady=(10, 0), sticky="w")
    
    # Appearance mode dropdown
    appearance_option_menu = create_button(
        parent,
        values=["Light", "Dark", "System"],
        command=callback,
        is_dropdown=True
    )
    appearance_option_menu.grid(row=start_row+1, column=0, padx=DEFAULT_PADDING, pady=(0, 10), sticky="ew")
    
    # Set default value
    appearance_option_menu.set("Dark")
    
    return appearance_label, appearance_option_menu

def create_drop_zone(parent: Any, 
                    handle_drop_callback: Callable[[Any], None], 
                    select_directory_callback: Callable[[Optional[Any]], None]) -> ctk.CTkLabel:
    """
    Create the drop zone for files.
    
    Args:
        parent: The parent frame
        handle_drop_callback: Callback for drop events
        select_directory_callback: Callback for directory selection
        
    Returns:
        widget: The drop zone widget
    """
    # Create drop zone label
    drop_label = create_label(
        parent,
        text=TEXTS["drop_zone_default"],
        font_size=20,  
        is_title=True,
        fg_color=("#F8F0F2", "#6A6D70"),  # Very light pink in light mode, lighter gray in dark mode
        height=120,  
        corner_radius=8
    )
    drop_label.pack(fill="x", padx=DEFAULT_PADDING, pady=DEFAULT_PADDING)
    
    # Add click event to select directory
    drop_label.bind("<Button-1>", lambda e: select_directory_callback(None))
    
    # Define enter/leave event handlers for hover effect
    def _on_enter(e: WidgetEvent) -> None:
        """Handle mouse enter event."""
        drop_label.configure(
            text=TEXTS["drop_zone_hover"],
            fg_color=("#F0E8EA", "#7A7D80")  # Slightly darker on hover
        )
    
    def _on_leave(e: Optional[WidgetEvent] = None) -> None:
        """Handle mouse leave event."""
        drop_label.configure(
            text=TEXTS["drop_zone_default"],
            fg_color=("#F8F0F2", "#6A6D70")  # Back to original color
        )
    
    drop_label.bind("<Enter>", _on_enter)
    drop_label.bind("<Leave>", _on_leave)
    
    # Initial styling
    _on_leave(None)
    
    return drop_label

def create_action_buttons(parent: Any, 
                         process_callback: Callable[[], None], 
                         save_callback: Callable[[], None]) -> Tuple[ctk.CTkFrame, List[ctk.CTkButton]]:
    """
    Create action buttons for processing files.
    
    Args:
        parent: The parent frame
        process_callback: Callback for processing files
        save_callback: Callback for saving files
        
    Returns:
        Tuple containing:
            - frame: The buttons frame
            - buttons: List of created buttons
    """
    # Create buttons frame
    buttons_frame = create_frame(parent)
    buttons_frame.pack(fill="x", padx=DEFAULT_PADDING, pady=(0, DEFAULT_PADDING))
    
    # Process button
    process_button = create_button(
        buttons_frame,
        text=TEXTS["button_process"],
        command=process_callback,
        font_size=DEFAULT_FONT_SIZE + 2
    )
    process_button.pack(side="left", padx=DEFAULT_PADDING, pady=DEFAULT_PADDING, fill="x", expand=True)
    
    # Save button
    save_button = create_button(
        buttons_frame,
        text=TEXTS["button_save"],
        command=save_callback,
        font_size=DEFAULT_FONT_SIZE + 2
    )
    save_button.pack(side="right", padx=DEFAULT_PADDING, pady=DEFAULT_PADDING, fill="x", expand=True)
    
    # Return both the frame and the buttons for theme updates
    return buttons_frame, [process_button, save_button]

def create_preview_section(parent: Any, 
                          width: Optional[int] = None, 
                          height: Optional[int] = None) -> ctk.CTkTextbox:
    """
    Create the preview section for displaying file list.
    
    Args:
        parent: The parent frame
        width: Optional width for the preview area
        height: Optional height for the preview area
        
    Returns:
        The preview text widget
    """
    # Preview text area
    preview_text = create_button(
        parent,
        text="",
        is_textbox=True,
        font_size=DEFAULT_FONT_SIZE,
        width=width if width else 200,
        height=height if height else 100
    )
    
    # Make read-only
    preview_text.configure(state="disabled")
    
    return preview_text

def setup_drag_drop(widget: Any, callback: Callable[[Any], None]) -> None:
    """
    Set up drag and drop functionality for a widget.
    
    Args:
        widget: The widget to set up drag and drop for
        callback: The callback function to call when files are dropped
    """
    # Register the widget with TkinterDnD
    widget.drop_target_register(DND_FILES)
    
    # Bind the callback to the drop event
    widget.dnd_bind('<<Drop>>', callback)

def update_button_colors(buttons: List[ctk.CTkButton], 
                        fg_color: Optional[str], 
                        hover_color: Optional[str]) -> None:
    """
    Update all button colors to match the current theme.
    
    Args:
        buttons: List of buttons to update
        fg_color: The foreground color for buttons
        hover_color: The hover color for buttons
    """
    for button in buttons:
        if isinstance(button, ctk.CTkButton):
            button.configure(fg_color=fg_color, hover_color=hover_color)
