#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Constants for the Code Processor application.
"""

# UI Constants
APP_TITLE = "✨ Code Processor for AI ✨"
APP_SIZE = "900x350"
APP_MIN_SIZE = (800, 300)
CONSOLE_FONT = ("Consolas", 14)
DEFAULT_PADDING = 5
DEFAULT_FONT_SIZE = 15
DEFAULT_BUTTON_HEIGHT = 30
TITLE_COLOR = "#5D0024"  # Dark red/violet color for titles
TITLE_BG_COLOR = "#E6D0D6"  # Light background for titles

# Supported file types and their language mappings
SUPPORTED_FILE_TYPES = {
    '.java': 'Java',
    '.py': 'Python',
    '.html': 'HTML',
    '.htm': 'HTML',
    '.js': 'JavaScript',
    '.css': 'CSS',
    '.xml': 'XML',
    '.sql': 'SQL',
    '.json': 'JSON',
    '.properties': 'Properties',
    '.jsp': 'JSP'
}

# AI Platform URLs and icons
AI_PLATFORMS = {
    'Grok': ('https://x.ai/grok', '🤖'),
    'ChatGPT': ('https://chat.openai.com', '💬'),
    'Gemini': ('https://gemini.google.com', '🌟'),
    'Claude': ('https://claude.ai', '🧠'),
    'Copilot': ('https://copilot.microsoft.com', '👨‍💻')
}
