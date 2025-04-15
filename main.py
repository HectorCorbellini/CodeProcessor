#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Code Processor for AI
A utility for processing code files to be shared with AI platforms.
"""

import os
import tkinter as tk
from tkinter import filedialog, messagebox
from typing import Any, List, Optional, Tuple, Union
import customtkinter as ctk
from tkinterdnd2 import DND_FILES, TkinterDnD

# Import the centralized logger
from logger import get_logger

# Get module logger
logger = get_logger(__name__)

# Import from modular components
from constants import (
    APP_SIZE, APP_MIN_SIZE, DEFAULT_PADDING, 
    DEFAULT_FONT_SIZE, DEFAULT_BUTTON_HEIGHT, AI_PLATFORMS
)
from helpers import (
    open_url, copy_to_clipboard, save_to_file, 
    get_file_language, change_appearance_mode, select_directory
)
from file_processor import (
    process_directory,
    format_files_for_ai,
    parse_dropped_files
)
from ui_components import (
    create_right_sidebar, create_appearance_mode_section, 
    create_drop_zone, create_action_buttons, create_preview_section,
    setup_drag_drop, update_button_colors
)
from ui_factory import create_label, create_frame, create_button
from texts import TEXTS

# Set appearance mode and default color theme
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")


class CodeProcessorApp:
    """
    Main application class for the Code Processor.
    Handles the UI and processing of code files.
    """
    
    def __init__(self, root: TkinterDnD.Tk) -> None:
        """
        Initialize the application.
        
        Args:
            root: The root Tkinter window
        """
        logger.info("Initializing CodeProcessorApp")
        self.root = root
        self.root.title(TEXTS["app_title"])
        self.root.geometry(APP_SIZE)
        self.root.minsize(*APP_MIN_SIZE)
        
        # Set window icon if available
        self._setup_window_icon()
        
        # Configure grid layout
        self._configure_grid()
        
        # Variables
        self.files: List[Tuple[str, str]] = []
        self.processed_content: str = ""
        self.buttons: List[ctk.CTkButton] = []  # Keep track of buttons for theme updates
        
        # Create UI components
        self._create_right_sidebar()
        self._create_main_frame()
        logger.info("CodeProcessorApp initialization complete")
    
    def _setup_window_icon(self) -> None:
        """Set up the window icon."""
        try:
            icon_path = "code_icon.ico"
            if os.path.exists(icon_path):
                self.root.iconbitmap(icon_path)
            else:
                logger.warning(f"Icon file {icon_path} not found")
        except Exception as e:
            logger.error(f"Failed to set window icon: {str(e)}")
    
    def _configure_grid(self) -> None:
        """Configure the grid layout for the main window."""
        self.root.grid_columnconfigure(0, weight=1)  # Main content area
        self.root.grid_columnconfigure(1, weight=0)  # Right sidebar
        self.root.grid_rowconfigure(0, weight=1)
    
    def _create_right_sidebar(self) -> None:
        """Create the right sidebar with AI platform buttons."""
        # Create sidebar using the ui_components module
        self.right_sidebar, platform_buttons = create_right_sidebar(self.root, self)
        
        # Add platform buttons to our tracked buttons list for theme updates
        self.buttons.extend(platform_buttons)
        
        # Create appearance mode section
        self._create_appearance_mode_section(len(AI_PLATFORMS)+3)
    
    def _create_appearance_mode_section(self, start_row: int) -> None:
        """
        Create the appearance mode section in the right sidebar.
        
        Args:
            start_row: The row to start placing the appearance mode controls
        """
        # Create appearance mode section using the ui_components module
        self.appearance_label, self.appearance_option_menu = create_appearance_mode_section(
            self.right_sidebar, 
            start_row, 
            self.change_appearance_mode_event
        )
        
        # Add to buttons list for theme updates
        self.buttons.append(self.appearance_option_menu)
    
    def _create_main_frame(self) -> None:
        """Create the main content frame with file drop zone and preview area."""
        # Create main frame
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.grid(row=0, column=0, padx=DEFAULT_PADDING, pady=DEFAULT_PADDING, sticky="nsew")
        self.main_frame.pack_propagate(False)
        
        # Create drop zone section
        self._create_drop_zone_section()
        
        # Create preview section
        self._create_preview_section()

    def _create_drop_zone_section(self) -> None:
        """Create the drop zone and action buttons section."""
        # Create drop zone frame
        self.drop_zone_frame = ctk.CTkFrame(self.main_frame)
        self.drop_zone_frame.pack(fill="x", padx=DEFAULT_PADDING, pady=DEFAULT_PADDING)
        
        # Create drop zone
        self._create_drop_zone()
        
        # Create action buttons
        self._create_action_buttons()

    def _create_drop_zone(self) -> None:
        """Create the drop zone for files."""
        # Create drop zone using the ui_components module
        self.drop_label = create_drop_zone(
            self.drop_zone_frame, 
            self.handle_drop, 
            self.select_directory
        )
        
        # Setup drag and drop functionality
        self.setup_drag_drop(self.drop_label)

    def _create_action_buttons(self) -> None:
        """Create action buttons for processing files."""
        # Create action buttons using the ui_components module
        self.buttons_frame, action_buttons = create_action_buttons(
            self.drop_zone_frame, 
            process_callback=self.process_files,
            save_callback=self.save_as_txt
        )
        # Add the buttons to our tracked buttons list for theme updates
        self.buttons.extend(action_buttons)

    def _create_preview_section(self) -> None:
        """Create the preview section for displaying file list."""
        # Create preview frame
        self.preview_frame = ctk.CTkFrame(self.main_frame)
        self.preview_frame.pack(fill="both", expand=True, padx=DEFAULT_PADDING, pady=DEFAULT_PADDING)
        
        # Create preview label frame
        self.preview_label_frame = ctk.CTkFrame(self.preview_frame)
        self.preview_label_frame.pack(fill="x", padx=DEFAULT_PADDING, pady=DEFAULT_PADDING)
        
        # Create preview label
        self.preview_label = create_label(
            self.preview_label_frame,
            text=TEXTS["label_selected_files"],
            anchor="w",
            font_size=DEFAULT_FONT_SIZE,
            is_title=True
        )
        self.preview_label.pack(side="left", padx=(0, DEFAULT_PADDING))
        
        # Create buttons frame
        self.buttons_frame = ctk.CTkFrame(self.preview_label_frame)
        self.buttons_frame.pack(side="right")
        
        # Create About button
        self.about_button = create_button(
            self.buttons_frame,
            text="About",
            command=self.show_about,
            font_size=DEFAULT_FONT_SIZE
        )
        self.about_button.pack(side="left", padx=(0, DEFAULT_PADDING))
        self.buttons.append(self.about_button)  # Track for theme updates
        
        # Create Help button
        self.help_button = create_button(
            self.buttons_frame,
            text="Help",
            command=self.show_help,
            font_size=DEFAULT_FONT_SIZE
        )
        self.help_button.pack(side="left")
        self.buttons.append(self.help_button)  # Track for theme updates
        
        # Create preview text area using the ui_components module
        self.preview_text = create_preview_section(self.preview_frame)
        self.preview_text.pack(fill="both", expand=True, padx=DEFAULT_PADDING, pady=(0, DEFAULT_PADDING))
    
    def change_appearance_mode_event(self, new_appearance_mode: str) -> None:
        """
        Change the appearance mode of the application.
        
        Args:
            new_appearance_mode: The new appearance mode ("Light", "Dark", or "System")
        """
        logger.info(f"Changing appearance mode to {new_appearance_mode}")
        # Change appearance mode using the helpers module
        change_appearance_mode(new_appearance_mode)
        
        # Update button colors based on the new theme
        # System mode should detect the system theme and use appropriate colors
        if new_appearance_mode == "Light":
            fg_color = "green"
            hover_color = "dark green"
        elif new_appearance_mode == "System":
            # Check the actual system appearance and apply appropriate colors
            current_appearance = ctk.get_appearance_mode().lower()
            if current_appearance == "light":
                fg_color = "green"
                hover_color = "dark green"
            else:
                fg_color = "blue"
                hover_color = "dark blue"
        else:  # Dark mode
            fg_color = None
            hover_color = None
        
        # Update button colors
        update_button_colors(self.buttons, fg_color, hover_color)
    
    def setup_drag_drop(self, widget: Any) -> None:
        """
        Set up drag and drop functionality for a widget.
        
        Args:
            widget: The widget to enable drag and drop for
        """
        # Setup drag and drop functionality using ui_components module
        setup_drag_drop(widget, self.handle_drop)
    
    def handle_drop(self, event: Any) -> None:
        """
        Handle file drop events.
        
        Args:
            event: The drop event
        """
        logger.info("Handling file drop event")
        # Parse dropped files using the file_processor module
        paths = parse_dropped_files(event.data)
        
        if paths:
            # Process all directories
            for path in paths:
                self.process_directory(path)
    
    def select_directory(self, event: Optional[Any] = None) -> None:
        """
        Open a directory selection dialog.
        
        Args:
            event: The event that triggered this function (optional)
        """
        logger.info("Selecting directory")
        # Select directory using the helpers module
        directory = select_directory()
        if directory:
            self.process_directory(directory)
    
    def process_directory(self, directory: str) -> None:
        """
        Process a directory to find and list code files.
        
        Args:
            directory: The directory path to process
        """
        logger.info(f"Processing directory: {directory}")
        # Process directory using the file_processor module
        self.files = process_directory(directory)
        
        # Update UI after processing
        self._update_ui_after_directory_processing()
    
    def _update_ui_after_directory_processing(self) -> None:
        """Update UI elements after directory processing."""
        logger.debug("Updating UI after directory processing")
        # Enable text widget for editing
        self.preview_text.configure(state="normal")
        self.preview_text.delete("1.0", "end")
        
        # Add files to preview
        for _, rel_path in self.files:
            language = get_file_language(rel_path)
            self.preview_text.insert("end", f"{rel_path} ({language})\n")
        
        # Make read-only again
        self.preview_text.configure(state="disabled")
        logger.debug(f"UI updated with {len(self.files)} files")
    
    def process_files(self) -> None:
        """Process selected files and copy the formatted content to clipboard."""
        if not self.files:
            logger.warning("No files selected when trying to process files")
            messagebox.showinfo("Info", TEXTS["info_no_files"])
            return
        
        logger.info(f"Processing {len(self.files)} files")
        # Format files for AI using the file_processor module
        self.processed_content = format_files_for_ai(self.files)
        
        # Copy to clipboard using the helpers module
        if copy_to_clipboard(self.processed_content):
            logger.info("Files processed and copied to clipboard successfully")
            messagebox.showinfo("Success", TEXTS["success_clipboard"])
    
    def save_as_txt(self) -> None:
        """Save processed content to a text file."""
        if not self.processed_content:
            logger.warning("No processed content when trying to save as TXT")
            messagebox.showinfo("Info", TEXTS["info_no_content"])
            return
        
        logger.info("Saving processed content to TXT file")
        # Save to file using the helpers module
        if save_to_file(self.processed_content):
            logger.info("File saved successfully")
            messagebox.showinfo("Success", TEXTS["success_save"])
    
    def open_ai_platform(self, platform: str) -> None:
        """
        Open an AI platform in the default web browser.
        
        Args:
            platform: The name of the AI platform to open
        """
        try:
            url = AI_PLATFORMS.get(platform, (None, None))[0]
            if url:
                # Open URL using the helpers module
                open_url(url, platform)
            else:
                logger.error(f"No URL configured for {platform}")
                messagebox.showerror("Error", TEXTS["error_no_url"].format(platform=platform))
        except Exception as e:
            logger.error(f"Error opening {platform}", exc_info=True)
            messagebox.showerror("Error", TEXTS["error_opening_url"].format(platform=platform, error=str(e)))

    def show_help(self) -> None:
        """Show help information in a message box."""
        help_text = """
Code Processor for AI - Help

1. Select a directory containing code files by:
   - Dragging and dropping a directory onto the drop zone
   - Clicking the drop zone to browse for a directory

2. The selected files will be listed in the preview area

3. Click "Process Files" to:
   - Format the code for AI platforms
   - Copy the formatted code to clipboard

4. Click "Save to File" to save the formatted code to a text file

5. Use the AI Platform buttons to open your preferred AI platform
"""
        messagebox.showinfo("Help", help_text)

    def show_about(self) -> None:
        """Show about information from README.md in a message box."""
        about_text = """
Code Processor for AI

A desktop application for processing code files to be shared with AI platforms. 
This tool helps developers format their code in a way that's optimized for sharing 
with AI assistants like ChatGPT, Claude, Bard, and others.

Features:
- Drag and Drop Interface
- Multiple File Support
- AI Platform Integration
- Clipboard Integration
- File Export
- Syntax Highlighting
- Dark/Light Mode
- Internationalization
- Responsive UI

Author: Héctor Corbellini
Version: 1.0
License: MIT
"""
        messagebox.showinfo("About", about_text)


def main() -> None:
    """Main entry point for the application."""
    try:
        # Create customtkinter window
        root = TkinterDnD.Tk()
        app = CodeProcessorApp(root)
        root.mainloop()
    except Exception as e:
        logger.critical("Application failed to start", exc_info=True)
        messagebox.showerror("Critical Error", TEXTS["critical_error"].format(error=str(e)))


if __name__ == "__main__":
    main()