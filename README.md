# Code Processor for AI

![Code Processor](https://img.shields.io/badge/Code%20Processor-v1.0-blue)
![Python](https://img.shields.io/badge/Python-3.8%2B-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## About this project...

###### Author: Héctor Corbellini

A desktop application for processing code files to be shared with AI platforms. This tool helps developers format their code in a way that's optimized for sharing with AI assistants like ChatGPT, Claude, Bard, and others.

## 📋 Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Direct Running](#direct-running)
- [Creating Standalone Executable](#creating-standalone-executable)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Architecture](#architecture)
- [Internationalization](#internationalization)
- [Contributing](#contributing)
- [License](#license)

## ✨ Features

- **Drag and Drop Interface**: Easily drag and drop directories or files
- **Multiple File Support**: Process multiple code files at once
- **AI Platform Integration**: Quick links to popular AI platforms
- **Clipboard Integration**: Automatically copy formatted code to clipboard
- **File Export**: Save formatted code to a text file
- **Syntax Highlighting**: Recognizes and formats various programming languages
- **Dark/Light Mode**: Customizable appearance
- **Internationalization**: Support for English and Spanish
- **Responsive UI**: Clean, modern interface built with CustomTkinter

## 🔧 Installation

### Prerequisites

- Python 3.11.2 or higher (must be accessible as 'python3')
- pip (Python package installer)
- Virtual environment support

For detailed Python installation instructions for Puppy Linux distributions, please refer to [pyINSTALL.md](../pyINSTALL.md).

### Setup

1. Create and activate a virtual environment:
   ```bash

   python3 -m venv venv
   source venv/bin/activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python main.py
   ```

## 🚀 Direct Running

The application can be run directly from the project directory without cloning the repository, as long as the required dependencies are installed. This is particularly useful for quick testing or development purposes.

To run directly:
```bash
python main.py
```

## 📦 Creating Standalone Executable

You can create a standalone executable that can be distributed and run without requiring Python or any dependencies to be installed on the target system.

### Automatic Windows Build (via GitHub Actions)

The Windows executable is automatically built and released through GitHub Actions:

1. The Windows executable is built whenever changes are pushed to the main branch
2. The executable is available in two locations:
   - GitHub Releases: https://github.com/yourusername/CodeProcessor/releases
   - GitHub Actions Artifacts: https://github.com/yourusername/CodeProcessor/actions
3. The build process includes:
   - Setting up Python 3.11 on Windows
   - Installing required dependencies
   - Creating a single-file executable
   - Creating a GitHub release

### Manual Linux Build

1. Install PyInstaller:
   ```bash
   pip install pyinstaller
   ```

2. Create the executable:
   ```bash
   pyinstaller --onefile --windowed --name CodeProcessor main.py
   ```

3. The executable will be created in the `dist` directory:
   ```bash
   dist/CodeProcessor
   ```

   Note: The Linux executable is already available in the `dist` folder of this repository.

4. You can now distribute this executable to users who don't need to have Python installed.

## 🚀 Usage

### Linux/MacOS

1. **Launch the application** by running `python main.py`
2. **Select files** by either:
   - Dragging and dropping a directory onto the drop zone
   - Clicking the drop zone to open a file browser
3. **Process files** by clicking the "Process Files" button
4. The formatted code is **copied to your clipboard**
5. **Paste the code** into your preferred AI platform

### Windows

1. Download the Windows executable from:
   - GitHub Releases: https://github.com/HectorCorbellini/CodeProcessor/releases
   - GitHub Actions Artifacts: https://github.com/HectorCorbellini/CodeProcessor/actions
2. Extract the downloaded zip file
3. Double-click `CodeProcessor.exe` to launch the application
4. The application works the same way as the Linux/MacOS version
6. Optionally, **save the formatted code** to a text file

## 📁 Project Structure

```
CodeProcessor_Py-/
├── main.py                 # Main application entry point
├── app_config.py           # Application configuration manager
├── constants.py            # Constants and default values
├── error_handler.py        # Centralized error handling
├── file_processor.py       # File processing logic
├── file_utils.py           # File utility functions
├── helpers.py              # Helper functions
├── logger.py               # Logging configuration
├── texts.py                # Text constants for internationalization
├── ui_components.py        # UI component creation
├── ui_factory.py           # Factory for creating UI elements
└── README.md               # Project documentation
```

## 🏗️ Architecture

The Code Processor application follows a modular architecture with clear separation of concerns:

### Core Components

1. **Main Application (`main.py`)**: 
   - Initializes the application
   - Sets up the UI
   - Handles user interactions

2. **Configuration Management (`app_config.py`)**: 
   - Manages application settings
   - Handles language and appearance preferences

3. **File Processing (`file_processor.py`, `file_utils.py`)**: 
   - Processes directories and files
   - Formats code for AI platforms
   - Handles file operations

4. **UI Components (`ui_components.py`, `ui_factory.py`)**: 
   - Creates and manages UI elements
   - Implements drag and drop functionality
   - Handles appearance mode changes

5. **Internationalization (`texts.py`)**: 
   - Manages text constants in multiple languages
   - Provides language switching functionality

6. **Error Handling and Logging (`error_handler.py`, `logger.py`)**: 
   - Centralizes error handling
   - Configures logging throughout the application

### Design Patterns

- **Factory Pattern**: Used for creating UI components
- **Decorator Pattern**: Used for error handling
- **Singleton Pattern**: Used for configuration and logging

## 🌐 Internationalization

The application supports multiple languages through the `texts.py` module:

- Currently supported languages: English (en) and Spanish (es)
- Language can be changed programmatically through the `set_language` function
- All UI text is stored in language-specific dictionaries

To add a new language:
1. Create a new dictionary in `texts.py` (e.g., `FR_TEXTS`)
2. Add the language code to `LANGUAGE_TEXTS`
3. Implement language switching in the UI if desired

## 🤝 Contributing

Contributions are welcome! Here's how you can contribute:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Commit your changes: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature/your-feature-name`
5. Open a pull request

Please ensure your code follows the project's coding style and includes appropriate tests.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgements

- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) for the modern UI components
- [TkinterDnD2](https://github.com/pmgagne/tkinterdnd2) for drag and drop functionality
- [Pyperclip](https://github.com/asweigart/pyperclip) for clipboard operations

---

Created with ❤️ by Héctor Corbellini
