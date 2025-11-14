@echo off
echo ========================================
echo DocumentAI Build Script with LibreOffice
echo ========================================
echo.

REM Record build start time
set start_time=%time%

REM ========================================
REM Step 1: Build Frontend
REM ========================================
echo [Step 1/6] Building frontend...
cd frontend
call npm install
if errorlevel 1 (
    echo ERROR: Frontend dependency installation failed
    pause
    exit /b 1
)

call npm run build
if errorlevel 1 (
    echo ERROR: Frontend build failed
    pause
    exit /b 1
)
echo SUCCESS: Frontend build complete
cd ..
echo.

REM ========================================
REM Step 2: Build Backend (PyInstaller)
REM ========================================
echo [Step 2/6] Building backend...
cd backend

REM Activate virtual environment
if exist .venv\Scripts\activate.bat (
    call .venv\Scripts\activate.bat
) else (
    echo WARNING: Virtual environment not found. Using global Python
)

REM Check PyInstaller installation
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo Installing PyInstaller...
    pip install pyinstaller
)

REM Remove previous build results
if exist dist rd /s /q dist
if exist build rd /s /q build

REM Build with PyInstaller
pyinstaller ..\build-scripts\build-backend.spec
if errorlevel 1 (
    echo ERROR: Backend build failed
    pause
    exit /b 1
)
echo SUCCESS: Backend build complete
cd ..
echo.

REM ========================================
REM Step 3: Download LibreOffice Portable
REM ========================================
echo [Step 3/6] Preparing LibreOffice Portable...

if not exist libreoffice (
    echo Downloading LibreOffice Portable...
    echo.
    echo Please download LibreOffice Portable manually:
    echo 1. Go to: https://www.libreoffice.org/download/portable-versions/
    echo 2. Download: LibreOffice Portable (Windows)
    echo 3. Extract to: %cd%\libreoffice
    echo.
    echo Folder structure should be:
    echo   libreoffice\
    echo   +-- program\
    echo       +-- soffice.exe
    echo.
    echo Press any key when LibreOffice Portable is ready...
    pause
    
    if not exist libreoffice\program\soffice.exe (
        echo ERROR: soffice.exe not found in libreoffice\program\
        echo Please extract LibreOffice Portable correctly
        pause
        exit /b 1
    )
) else (
    echo SUCCESS: LibreOffice directory found
    
    if not exist libreoffice\program\soffice.exe (
        echo WARNING: soffice.exe not found
        echo Please check LibreOffice Portable installation
        pause
    ) else (
        echo SUCCESS: soffice.exe found
    )
)
echo.

REM ========================================
REM Step 4: Prepare Ollama
REM ========================================
echo [Step 4/6] Preparing Ollama...

if not exist ollama (
    echo WARNING: Ollama directory not found.
    echo.
    echo To include Ollama in the build:
    echo 1. Download from https://ollama.com/download
    echo 2. Copy ollama.exe to ollama/ folder
    echo 3. Copy models to ollama/models/
    echo.
    echo NOTE: Build will continue without Ollama.
    echo Users will need to install Ollama separately.
    echo.
    timeout /t 5
) else (
    echo SUCCESS: Ollama directory found
    
    if not exist ollama\models (
        echo WARNING: models directory not found in ollama/
        echo To download models: ollama pull mistral
        timeout /t 3
    ) else (
        echo SUCCESS: Models directory found
    )
)
echo.

REM ========================================
REM Step 5: Install Electron dependencies
REM ========================================
echo [Step 5/6] Installing Electron dependencies...
cd electron
call npm install
if errorlevel 1 (
    echo ERROR: Electron dependency installation failed
    pause
    exit /b 1
)
echo SUCCESS: Electron dependencies installed
cd ..
echo.

REM ========================================
REM Step 6: Build Electron app
REM ========================================
echo [Step 6/6] Building Electron app...
cd electron
call npm run build:win
if errorlevel 1 (
    echo ERROR: Electron build failed
    pause
    exit /b 1
)
echo SUCCESS: Electron build complete
cd ..
echo.

REM ========================================
REM Copy LibreOffice to dist
REM ========================================
echo Copying LibreOffice Portable to build output...
if exist libreoffice (
    if exist electron\dist\win-unpacked (
        echo Copying libreoffice to electron\dist\win-unpacked\libreoffice
        xcopy /E /I /Y libreoffice electron\dist\win-unpacked\libreoffice
        echo SUCCESS: LibreOffice copied
    )
)
echo.

REM ========================================
REM Build Complete
REM ========================================
echo ========================================
echo Build Complete!
echo ========================================
echo.
echo Build output location:
echo    - Installer: electron\dist\DocumentAI Setup.exe
echo    - Portable: electron\dist\win-unpacked\DocumentAI.exe
echo.
if not exist ollama (
    echo NOTE: Ollama was not included in this build.
    echo Users will need to install Ollama separately from:
    echo https://ollama.com/download
    echo.
)
if exist libreoffice (
    echo SUCCESS: LibreOffice Portable included in build
    echo HWP to PDF conversion will work without user installation
    echo.
) else (
    echo WARNING: LibreOffice was not included
    echo Users will need to install LibreOffice for HWP to PDF conversion
    echo.
)
echo Build completed at: %time%
echo Build started at: %start_time%
echo.
echo You can now run the installer or use the portable version.
echo.
pause
