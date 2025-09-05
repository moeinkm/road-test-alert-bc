@echo off
setlocal enabledelayedexpansion

REM Version configuration - easy to change in the future
set REQUIRED_PYTHON_VERSION=3.12
set REQUIRED_POSTGRES_VERSION=16

echo 🚀 Road Test Alert BC Backend - Windows Installation Script
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed or not in PATH
    echo.
    echo 🐍 Installing Python %REQUIRED_PYTHON_VERSION%...
    echo.
    
    REM Try to install Python using available package managers
    winget --version >nul 2>&1
    if %errorlevel% equ 0 (
        echo 🪟 Using Windows Package Manager (winget) to install Python...
        winget install Python.Python.%REQUIRED_PYTHON_VERSION%
        if %errorlevel% equ 0 (
                    echo ✅ Python installed successfully via winget
        echo 🔄 Refreshing PATH...
        call refreshenv >nul 2>&1 || echo ⚠️  PATH refresh failed - you may need to restart your terminal
        ) else (
            echo ⚠️  winget installation failed, trying alternative methods...
        )
    )
    
    REM If winget failed or not available, try chocolatey
    if %errorlevel% neq 0 (
        choco --version >nul 2>&1
        if %errorlevel% equ 0 (
            echo 🍫 Using Chocolatey to install Python...
            choco install python%REQUIRED_PYTHON_VERSION% -y
            if %errorlevel% equ 0 (
                            echo ✅ Python installed successfully via Chocolatey
            echo 🔄 Refreshing PATH...
            call refreshenv >nul 2>&1 || echo ⚠️  PATH refresh failed - you may need to restart your terminal
            ) else (
                echo ⚠️  Chocolatey installation failed
            )
        )
    )
    
    REM If both package managers failed, provide manual instructions
    python --version >nul 2>&1
    if %errorlevel% neq 0 (
        echo ❌ Automatic Python installation failed
        echo.
        echo 📥 Please install Python %REQUIRED_PYTHON_VERSION% manually:
        echo   1. Visit: https://www.python.org/downloads/
        echo   2. Download Python %REQUIRED_PYTHON_VERSION% for Windows
        echo   3. Run the installer (make sure to check "Add Python to PATH")
        echo   4. Restart this script
        echo.
        pause
        exit /b 1
    )
)

REM Check Python version
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
for /f "tokens=1 delims=." %%i in ("!PYTHON_VERSION!") do set PYTHON_MAJOR=%%i
for /f "tokens=2 delims=." %%i in ("!PYTHON_VERSION!") do set PYTHON_MINOR=%%i

if !PYTHON_MAJOR! neq 3 (
    echo ❌ Python 3 is required, found Python !PYTHON_VERSION!
    pause
    exit /b 1
)

for /f "tokens=2 delims=." %%i in ("%REQUIRED_PYTHON_VERSION%") do set REQUIRED_PYTHON_MINOR=%%i
if !PYTHON_MINOR! lss !REQUIRED_PYTHON_MINOR! (
    echo ❌ Python %REQUIRED_PYTHON_VERSION% or higher is required, found Python !PYTHON_VERSION!
    echo 📥 Please upgrade to Python %REQUIRED_PYTHON_VERSION% from: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo ✅ Python !PYTHON_VERSION! found

REM Check if PostgreSQL is installed
psql --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ PostgreSQL is not installed or not in PATH
    echo.
    echo 🐘 Installing PostgreSQL %REQUIRED_POSTGRES_VERSION%.x...
    echo.
    
    REM Try to install PostgreSQL using available package managers
    winget --version >nul 2>&1
    if %errorlevel% equ 0 (
        echo 🪟 Using Windows Package Manager (winget) to install PostgreSQL...
        winget install PostgreSQL.PostgreSQL
        if %errorlevel% equ 0 (
            echo ✅ PostgreSQL installed successfully via winget
            echo 🔄 Refreshing PATH...
            call refreshenv >nul 2>&1 || echo ⚠️  PATH refresh failed - you may need to restart your terminal
        ) else (
            echo ⚠️  winget installation failed, trying alternative methods...
        )
    )
    
    REM If winget failed or not available, try chocolatey
    if %errorlevel% neq 0 (
        choco --version >nul 2>&1
        if %errorlevel% equ 0 (
            echo 🍫 Using Chocolatey to install PostgreSQL...
            choco install postgresql -y
            if %errorlevel% equ 0 (
                echo ✅ PostgreSQL installed successfully via Chocolatey
                echo 🔄 Refreshing PATH...
                call refreshenv >nul 2>&1 || echo ⚠️  PATH refresh failed - you may need to restart your terminal
            ) else (
                echo ⚠️  Chocolatey installation failed
            )
        )
    )
    
    REM If both package managers failed, provide manual instructions
    psql --version >nul 2>&1
    if %errorlevel% neq 0 (
        echo ❌ Automatic PostgreSQL installation failed
        echo.
        echo 📥 Please install PostgreSQL %REQUIRED_POSTGRES_VERSION%.x manually:
        echo   1. Visit: https://www.postgresql.org/download/windows/
        echo   2. Download PostgreSQL %REQUIRED_POSTGRES_VERSION% for Windows
        echo   3. Run the installer (make sure to check "Add PostgreSQL to PATH")
        echo   4. Restart this script
        echo.
        pause
        exit /b 1
    )
) else (
    REM Check PostgreSQL version
    for /f "tokens=3" %%i in ('psql --version 2^>^&1') do set POSTGRES_VERSION=%%i
    for /f "tokens=1 delims=." %%i in ("!POSTGRES_VERSION!") do set POSTGRES_MAJOR=%%i
    
    if !POSTGRES_MAJOR! lss %REQUIRED_POSTGRES_VERSION% (
        echo ❌ PostgreSQL %REQUIRED_POSTGRES_VERSION%.x or higher is required, found PostgreSQL !POSTGRES_VERSION!
        echo 📥 Please upgrade to PostgreSQL %REQUIRED_POSTGRES_VERSION% from: https://www.postgresql.org/download/windows/
        pause
        exit /b 1
    )
    
    echo ✅ PostgreSQL !POSTGRES_VERSION! found (compatible with %REQUIRED_POSTGRES_VERSION%)
    
    REM Check if PostgreSQL is in PATH for current session
    psql --version >nul 2>&1
    if %errorlevel% neq 0 (
        echo ⚠️  PostgreSQL found but not in PATH for current session
        echo 🔧 Adding PostgreSQL to PATH permanently...
        
        REM Add to user PATH environment variable
        setx PATH "%PATH%;C:\Program Files\PostgreSQL\%REQUIRED_POSTGRES_VERSION%\bin" >nul 2>&1
        if %errorlevel% equ 0 (
            echo ✅ Added PostgreSQL to PATH permanently
            echo 💡 Restart your terminal for changes to take effect
        ) else (
            echo ⚠️  Failed to add PostgreSQL to PATH automatically
            echo 💡 Please add PostgreSQL bin directory to PATH manually:
            echo    C:\Program Files\PostgreSQL\%REQUIRED_POSTGRES_VERSION%\bin
        )
    ) else (
        echo ✅ PostgreSQL is accessible in current session
    )
)

REM Check if pipenv is installed
pipenv --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 📦 Installing pipenv...
    pip install --user pipenv
    if %errorlevel% neq 0 (
        echo ❌ Failed to install pipenv
        pause
        exit /b 1
    fi
    echo ✅ pipenv installed successfully
) else (
    echo ✅ pipenv found
)

echo 🔧 Setting up project dependencies...

REM Check if virtual environment already exists and has dependencies
if exist "Pipfile" (
    echo 📋 Found existing Pipfile, checking if virtual environment is set up...
    
    REM Try to activate and check if dependencies are installed
    pipenv run python -c "import fastapi" >nul 2>&1
    if %errorlevel% equ 0 (
        echo ✅ Virtual environment already set up with dependencies
        echo 🚀 Ready to use! Run: pipenv shell
        goto :success
    ) else (
        echo ⚠️  Virtual environment exists but dependencies may be missing or outdated
    )
)

REM For development, we prefer installing from Pipfile to get latest compatible versions
REM Only use Pipfile.lock as a fallback if there are issues
echo 📦 Installing dependencies from Pipfile (development mode)...
echo 💡 This will install the latest compatible versions of packages

pipenv install --dev
if %errorlevel% neq 0 (
    echo ⚠️  Installation from Pipfile failed, trying with lock file as fallback...
    
    REM Check for existing Pipfile.lock and handle Windows-specific issues
    if exist Pipfile.lock (
        echo 📋 Found existing Pipfile.lock, checking for compatibility...
        
        REM Check for macOS/Linux specific packages that might cause issues on Windows
        findstr /i "pywinpty\|winpty" Pipfile.lock >nul 2>&1
        if %errorlevel% equ 0 (
            echo ⚠️  Detected potential compatibility issues in lock file
            echo 🔄 Removing lock file to regenerate for Windows...
            del Pipfile.lock
        )
    )
    
    REM Try installing with lock file as fallback
    pipenv install --dev
    if %errorlevel% neq 0 (
        echo ❌ Failed to install dependencies. Trying minimal installation...
        
        REM Install only essential packages
        pipenv install fastapi uvicorn sqlalchemy psycopg2-binary python-jose passlib python-multipart email-validator python-dotenv bcrypt pydantic pydantic-settings alembic pytest httpx starlette requests pytest-snapshot pytest-cov
        
        if %errorlevel% neq 0 (
            echo ❌ Minimal installation also failed
            pause
            exit /b 1
        )
        
        echo ⚠️  Minimal installation completed. Some dev dependencies may be missing.
    )
)

:success
echo.
echo 🎉 Installation completed successfully!
echo.
echo 🚀 Next steps:
echo    1. Set up your environment configuration:
echo       - Copy .env.example to .env: copy .env.example .env
echo       - Edit .env with your actual values (database, secrets, etc.)
echo       - Never commit .env to version control
echo    2. For Docker development:
echo       - Configure database settings in .env
echo       - Run: make up
echo    3. For native development:
echo       - Configure database settings in .env
echo       - Run: pipenv shell && uvicorn app.main:app --reload
echo.
echo 📖 For detailed environment setup, see: README.md
echo 🔒 Security: Keep your .env file secure and never share it
echo.
pause
