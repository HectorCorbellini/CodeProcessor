#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Text constants for internationalization of the Code Processor application.
"""

from logger import get_logger
from app_config import AppConfig

# Get module logger
logger = get_logger(__name__)

# English text constants
EN_TEXTS = {
    # UI Elements
    "app_title": "✨ Code Processor for AI ✨",
    "title_ai_platforms": "AI Platforms",
    "title_appearance": "Appearance Mode",
    "button_process": "Process Files",
    "button_save": "Save to File",
    "button_close": "Close",
    "label_selected_files": "Selected Files",
    "drop_zone_default": "📁 Drop directory here or click to select",
    "drop_zone_active": "📂 Drop files/folders here...",
    "drop_zone_hover": "📂 Click to browse files...",
    
    # Messages
    "info_no_files": "No files selected. Please select a directory first.",
    "info_no_content": "No processed content. Please process files first.",
    "info_clipboard": "Code copied to clipboard!",
    "info_save_success": "File saved successfully!",
    "success_clipboard": "Code processed and copied to clipboard!",
    "success_save": "File saved successfully!",
    "critical_error": "Application failed to start: {error}",
    
    # File Processing
    "file_path": "**File: {path}**",
    "file_language": "**Language: {language}**",
    "file_error_content": "**Error: Could not read file content**",
    "file_error_read": "**Error reading file: {error}**",
    "file_error_format": "**Error formatting files: {error}**",
    
    # Errors
    "error_opening_url": "Error opening {platform}: {error}",
    "error_no_url": "No URL configured for {platform}",
    "error_clipboard": "Error copying to clipboard: {error}",
    "error_save_file": "Error saving to file: {error}",
    "error_processing_directory": "Error processing directory: {error}",
    "error_formatting_code": "Error formatting code: {error}",
    "error_parsing_dropped_files": "Error parsing dropped files: {error}"
}

# Spanish text constants
ES_TEXTS = {
    # UI Elements
    "app_title": "✨ Procesador de Código para IA ✨",
    "title_ai_platforms": "Plataformas de IA",
    "title_appearance": "Modo de Apariencia",
    "button_process": "Procesar Archivos",
    "button_save": "Guardar a Archivo",
    "button_close": "Cerrar",
    "label_selected_files": "Archivos Seleccionados",
    "drop_zone_default": "📁 Arrastre directorio aquí o haga clic para seleccionar",
    "drop_zone_active": "📂 Suelta archivos/carpetas aquí...",
    "drop_zone_hover": "📂 Haga clic para explorar archivos...",
    
    # Messages
    "info_no_files": "No hay archivos seleccionados. Por favor, selecciona un directorio primero.",
    "info_no_content": "No hay contenido procesado. Por favor, procese los archivos primero.",
    "info_clipboard": "¡Código copiado al portapapeles!",
    "info_save_success": "¡Archivo guardado exitosamente!",
    "success_clipboard": "¡Código procesado y copiado al portapapeles!",
    "success_save": "¡Archivo guardado exitosamente!",
    "critical_error": "Error al iniciar la aplicación: {error}",
    
    # File Processing
    "file_path": "**Archivo: {path}**",
    "file_language": "**Lenguaje: {language}**",
    "file_error_content": "**Error: No se pudo leer el contenido del archivo**",
    "file_error_read": "**Error al leer el archivo: {error}**",
    "file_error_format": "**Error al formatear archivos: {error}**",
    
    # Errors
    "error_opening_url": "Error al abrir {platform}: {error}",
    "error_no_url": "No hay URL configurada para {platform}",
    "error_clipboard": "Error al copiar al portapapeles: {error}",
    "error_save_file": "Error al guardar en archivo: {error}",
    "error_processing_directory": "Error al procesar directorio: {error}",
    "error_formatting_code": "Error al formatear código: {error}",
    "error_parsing_dropped_files": "Error al analizar archivos soltados: {error}"
}

# Dictionary mapping language codes to text dictionaries
LANGUAGE_TEXTS = {
    "en": EN_TEXTS,
    "es": ES_TEXTS
}

# Current active texts dictionary
TEXTS = EN_TEXTS

def set_language(language_code: str) -> bool:
    """
    Set the application language.
    
    Args:
        language_code: Language code ('en' or 'es')
        
    Returns:
        bool: True if successful, False if language not supported
    """
    global TEXTS
    
    if language_code in LANGUAGE_TEXTS:
        TEXTS = LANGUAGE_TEXTS[language_code]
        AppConfig.set_language(language_code)
        logger.info(f"Language set to {language_code}")
        return True
    else:
        logger.warning(f"Unsupported language: {language_code}")
        return False

# Initialize language from config
current_language = AppConfig.get_language()
if current_language != "en":  # Only change if not the default
    set_language(current_language)
