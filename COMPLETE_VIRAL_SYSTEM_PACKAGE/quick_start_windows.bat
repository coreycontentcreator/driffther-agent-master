@echo off
REM ===========================================================
REM VIRAL YOUTUBE DOCUMENTARY SYSTEM - Windows Quick Start
REM ===========================================================
REM
REM This script automatically sets up everything you need!
REM Just double-click this file to run it.
REM
REM What it does:
REM 1. Checks if Python is installed
REM 2. Creates a virtual environment
REM 3. Installs all required packages
REM 4. Creates configuration files
REM 5. Tests the installation
REM
REM ===========================================================

echo.
echo ========================================
echo   VIRAL DOCUMENTARY SYSTEM SETUP
echo ========================================
echo.

REM Check if Python is installed
echo [1/6] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed!
    echo.
    echo Please install Python 3.11 or higher from:
    echo https://www.python.org/downloads/
    echo.
    echo Make sure to check "Add Python to PATH" during installation!
    pause
    exit /b 1
)

python --version
echo ✓ Python is installed!
echo.

REM Check Python version
echo [2/6] Verifying Python version...
python -c "import sys; exit(0 if sys.version_info >= (3, 11) else 1)"
if errorlevel 1 (
    echo ERROR: Python 3.11+ required!
    echo Your version is too old. Please upgrade Python.
    pause
    exit /b 1
)
echo ✓ Python version is compatible!
echo.

REM Create virtual environment
echo [3/6] Creating virtual environment...
if exist venv (
    echo Virtual environment already exists, skipping...
) else (
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment!
        pause
        exit /b 1
    )
    echo ✓ Virtual environment created!
)
echo.

REM Activate virtual environment
echo [4/6] Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment!
    pause
    exit /b 1
)
echo ✓ Virtual environment activated!
echo.

REM Upgrade pip
echo [5/6] Upgrading pip...
python -m pip install --upgrade pip --quiet
echo ✓ Pip upgraded!
echo.

REM Install requirements
echo [6/6] Installing required packages...
echo This may take 5-10 minutes depending on your internet speed...
echo.
pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo ERROR: Package installation failed!
    echo.
    echo Common fixes:
    echo 1. Check your internet connection
    echo 2. Try running: pip install --upgrade pip
    echo 3. Install Visual Studio Build Tools if on Windows
    echo.
    pause
    exit /b 1
)
echo.
echo ✓ All packages installed!
echo.

REM Create .env file if it doesn't exist
echo Creating configuration files...
if not exist .env (
    (
        echo # Viral YouTube Documentary System - Environment Variables
        echo.
        echo # REQUIRED: Anthropic Claude API Key
        echo # Get your key at: https://console.anthropic.com/
        echo ANTHROPIC_API_KEY=your_anthropic_api_key_here
        echo.
        echo # REQUIRED: OpenAI API Key (for embeddings)
        echo # Get your key at: https://platform.openai.com/api-keys
        echo OPENAI_API_KEY=your_openai_api_key_here
        echo.
        echo # OPTIONAL: JSTOR API Key (for academic research)
        echo # Apply at: https://about.jstor.org/whats-in-jstor/text-mining-support/
        echo JSTOR_API_KEY=your_jstor_api_key_here
        echo.
        echo # OPTIONAL: Semantic Scholar API Key
        echo SEMANTIC_SCHOLAR_API_KEY=
        echo.
        echo # OPTIONAL: YouTube API Key
        echo YOUTUBE_API_KEY=
    ) > .env
    echo ✓ Created .env file
) else (
    echo .env file already exists, skipping...
)

REM Copy config example
if not exist config\config.yaml (
    if exist config\config.example.yaml (
        copy config\config.example.yaml config\config.yaml >nul
        echo ✓ Created config.yaml from template
    )
) else (
    echo config.yaml already exists, skipping...
)
echo.

REM Create necessary directories
echo Creating project directories...
if not exist logs mkdir logs
if not exist backups mkdir backups
if not exist chroma_db mkdir chroma_db
if not exist outputs mkdir outputs
echo ✓ Directories created!
echo.

echo ========================================
echo   SETUP COMPLETE! 🎉
echo ========================================
echo.
echo NEXT STEPS:
echo.
echo 1. ADD YOUR API KEYS:
echo    - Open .env file in a text editor
echo    - Add your Anthropic API key
echo    - Add your OpenAI API key
echo.
echo 2. TEST THE SYSTEM:
echo    - Run: python scripts\quick_test.py
echo.
echo 3. START CREATING:
echo    - Run: python scripts\generate_documentary.py
echo.
echo DOCUMENTATION:
echo    - Read: README.md (getting started)
echo    - Read: docs\MULTI_AGENT_SYSTEM_SUMMARY.md (system overview)
echo.
echo ========================================
echo.
echo Virtual environment is now active!
echo To deactivate it, type: deactivate
echo.
pause
