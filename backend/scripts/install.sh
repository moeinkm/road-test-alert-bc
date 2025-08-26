#!/usr/bin/env bash
set -euo pipefail

# Version configuration - easy to change in the future
REQUIRED_PYTHON_VERSION="3.12"
REQUIRED_POSTGRES_VERSION="16"

# Check if Python 3.12 is installed

check_python_version() {
  local python_version
  python_version=$(python3 -c "import sys; print('.'.join(map(str, sys.version_info[:2])))" 2>/dev/null)
  
  if [[ $? -eq 0 ]]; then
    if [[ "$python_version" == "$REQUIRED_PYTHON_VERSION" ]]; then
      echo "✅ Python $REQUIRED_PYTHON_VERSION found"
      return 0
    else
      echo "⚠️  Python $python_version found, but $REQUIRED_PYTHON_VERSION is required"
      return 1
    fi
  else
    echo "❌ Python 3 not found"
    return 1
  fi
}

# Check if Python 3.12 is installed
if ! check_python_version; then
  echo "🐍 Python $REQUIRED_PYTHON_VERSION not found. Installing Python $REQUIRED_PYTHON_VERSION..."
  
  # Check OS and install Python accordingly
  if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS - use Homebrew if available, otherwise provide guidance
    if command -v brew >/dev/null 2>&1; then
      echo "📦 Installing Python $REQUIRED_PYTHON_VERSION via Homebrew..."
      
      # Check if Python is already installed via Homebrew
      if brew list python@$REQUIRED_PYTHON_VERSION >/dev/null 2>&1; then
        echo "✅ Python $REQUIRED_PYTHON_VERSION already installed via Homebrew"
        echo "🔄 Updating PATH to use Homebrew Python..."
        export PATH="/opt/homebrew/bin:$PATH"
      else
        brew install python@$REQUIRED_PYTHON_VERSION
        export PATH="/opt/homebrew/bin:$PATH"
      fi
    else
      echo "❌ Homebrew not found. Please install Python $REQUIRED_PYTHON_VERSION manually:"
      echo ""
      echo "Option 1: Install Homebrew first, then run this script again:"
      echo "   /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
      echo ""
      echo "Option 2: Install Python directly:"
      echo "   Visit: https://www.python.org/downloads/"
      echo "   Download and install Python $REQUIRED_PYTHON_VERSION for macOS"
      echo ""
      echo "Option 3: Use pyenv (Python version manager):"
      echo "   brew install pyenv"
      echo "   pyenv install $REQUIRED_PYTHON_VERSION"
      echo "   pyenv global $REQUIRED_PYTHON_VERSION"
      echo ""
      exit 1
    fi
  elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux - try package manager
    if command -v apt-get >/dev/null 2>&1; then
      echo "📦 Installing Python $REQUIRED_PYTHON_VERSION via apt..."
      
      # Check if Python is already installed
      if command -v python3.$REQUIRED_PYTHON_VERSION >/dev/null 2>&1; then
        echo "✅ Python $REQUIRED_PYTHON_VERSION already installed"
        # Create symlink if needed
        if [[ ! -f /usr/bin/python3 ]]; then
          sudo ln -sf /usr/bin/python3.$REQUIRED_PYTHON_VERSION /usr/bin/python3
        fi
      else
        sudo apt-get update && sudo apt-get install -y python3.$REQUIRED_PYTHON_VERSION python3.$REQUIRED_PYTHON_VERSION-pip
        # Create symlink if needed
        if [[ ! -f /usr/bin/python3 ]]; then
          sudo ln -sf /usr/bin/python3.$REQUIRED_PYTHON_VERSION /usr/bin/python3
        fi
      fi
    elif command -v yum >/dev/null 2>&1; then
      echo "📦 Installing Python $REQUIRED_PYTHON_VERSION via yum..."
      
      # Check if Python is already installed
      if command -v python3.$REQUIRED_PYTHON_VERSION >/dev/null 2>&1; then
        echo "✅ Python $REQUIRED_PYTHON_VERSION already installed"
      else
        sudo yum install -y python3.$REQUIRED_PYTHON_VERSION python3.$REQUIRED_PYTHON_VERSION-pip
      fi
    elif command -v dnf >/dev/null 2>&1; then
      echo "📦 Installing Python $REQUIRED_PYTHON_VERSION via dnf..."
      
      # Check if Python is already installed
      if command -v python3.$REQUIRED_PYTHON_VERSION >/dev/null 2>&1; then
        echo "✅ Python $REQUIRED_PYTHON_VERSION already installed"
      else
        sudo dnf install -y python3.$REQUIRED_PYTHON_VERSION python3.$REQUIRED_PYTHON_VERSION-pip
      fi
    else
      echo "❌ Unsupported Linux distribution. Please install Python $REQUIRED_PYTHON_VERSION manually."
      exit 1
    fi
  elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "cygwin" ]]; then
    # Windows - provide guidance
    echo "🪟 Windows detected. Please install Python $REQUIRED_PYTHON_VERSION manually:"
    echo "   Visit: https://www.python.org/downloads/"
    echo "   Or use Windows Package Manager: winget install Python.Python.3.12"
    echo "   Or use Chocolatey: choco install python312"
    exit 1
  else
    echo "❌ Unsupported OS: $OSTYPE. Please install Python $REQUIRED_PYTHON_VERSION manually."
    exit 1
  fi
  
  # Verify installation
  if check_python_version; then
    echo "✅ Python $REQUIRED_PYTHON_VERSION installed successfully"
  else
    echo "❌ Failed to install Python $REQUIRED_PYTHON_VERSION. Please install manually."
    exit 1
  fi
fi

# Check if PostgreSQL is installed
check_postgres_version() {
  local postgres_version
  local postgres_major
  
  echo "  🔍 Looking for psql command..."
  if command -v psql >/dev/null 2>&1; then
    echo "  ✅ psql command found"
    postgres_version=$(psql --version | grep -oE '[0-9]+\.[0-9]+' | head -1)
    echo "  📋 PostgreSQL version: $postgres_version"
    postgres_major=$(echo "$postgres_version" | cut -d. -f1)
    echo "  📋 PostgreSQL major version: $postgres_major (required: $REQUIRED_POSTGRES_VERSION)"
    
    if [[ "$postgres_major" == "$REQUIRED_POSTGRES_VERSION" ]]; then
      echo "✅ PostgreSQL $postgres_version found (compatible with $REQUIRED_POSTGRES_VERSION)"
      return 0
    else
      echo "⚠️  PostgreSQL $postgres_version found, but $REQUIRED_POSTGRES_VERSION.x is required"
      return 1
    fi
  else
    echo "  ❌ psql command not found in PATH"
    echo "❌ PostgreSQL not found"
    return 1
  fi
}

# Install PostgreSQL based on OS
install_postgres() {
  echo "🐘 PostgreSQL $REQUIRED_POSTGRES_VERSION.x not found. Installing PostgreSQL $REQUIRED_POSTGRES_VERSION..."
  echo "  🖥️  Detected OS: $OSTYPE"
  
  if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS - use Homebrew
    echo "  🔍 Checking for Homebrew..."
    if command -v brew >/dev/null 2>&1; then
      echo "  ✅ Homebrew found"
      echo "📦 Installing PostgreSQL $REQUIRED_POSTGRES_VERSION via Homebrew..."
      
      if brew list postgresql@$REQUIRED_POSTGRES_VERSION >/dev/null 2>&1; then
        echo "✅ PostgreSQL $REQUIRED_POSTGRES_VERSION already installed via Homebrew"
      else
        brew install postgresql@$REQUIRED_POSTGRES_VERSION
        echo "🔄 Starting PostgreSQL service..."
        brew services start postgresql@$REQUIRED_POSTGRES_VERSION
      fi
      
      # Add to PATH and check if installation worked
      export PATH="/opt/homebrew/opt/postgresql@$REQUIRED_POSTGRES_VERSION/bin:$PATH"
      
      # Verify the installation worked
      if ! command -v psql >/dev/null 2>&1; then
        echo "❌ PostgreSQL installation failed - psql command not found in PATH"
        echo "💡 Try restarting your terminal or manually add to PATH:"
        echo "   export PATH=\"/opt/homebrew/opt/postgresql@$REQUIRED_POSTGRES_VERSION/bin:\$PATH\""
        echo "💡 To make this permanent, add to your shell profile (~/.zshrc or ~/.bash_profile):"
        echo "   echo 'export PATH=\"/opt/homebrew/opt/postgresql@$REQUIRED_POSTGRES_VERSION/bin:\$PATH\"' >> ~/.zshrc"
        exit 1
      fi
      
      # Add PostgreSQL to shell profile permanently
      echo "🔧 Adding PostgreSQL to shell profile for permanent access..."
      SHELL_PROFILE=""
      if [[ -f "$HOME/.zshrc" ]]; then
        SHELL_PROFILE="$HOME/.zshrc"
      elif [[ -f "$HOME/.bash_profile" ]]; then
        SHELL_PROFILE="$HOME/.bash_profile"
      elif [[ -f "$HOME/.bashrc" ]]; then
        SHELL_PROFILE="$HOME/.bashrc"
      else
        SHELL_PROFILE="$HOME/.zshrc"
        touch "$SHELL_PROFILE"
      fi
      
      # Check if PATH is already added to avoid duplicates
      PATH_LINE="export PATH=\"/opt/homebrew/opt/postgresql@$REQUIRED_POSTGRES_VERSION/bin:\$PATH\""
      if ! grep -q "postgresql@$REQUIRED_POSTGRES_VERSION/bin" "$SHELL_PROFILE" 2>/dev/null; then
        echo "" >> "$SHELL_PROFILE"
        echo "# PostgreSQL $REQUIRED_POSTGRES_VERSION - Added by install script" >> "$SHELL_PROFILE"
        echo "$PATH_LINE" >> "$SHELL_PROFILE"
        echo "✅ Added PostgreSQL to $SHELL_PROFILE"
        
        # Export PATH for current session
        export PATH="/opt/homebrew/opt/postgresql@$REQUIRED_POSTGRES_VERSION/bin:$PATH"
        echo "✅ PostgreSQL is now available in current session"
      else
        echo "✅ PostgreSQL PATH already configured in $SHELL_PROFILE"
        # Export PATH for current session
        export PATH="/opt/homebrew/opt/postgresql@$REQUIRED_POSTGRES_VERSION/bin:$PATH"
      fi
    else
      echo "❌ Homebrew not found. Please install PostgreSQL $REQUIRED_POSTGRES_VERSION manually:"
      echo "   Visit: https://www.postgresql.org/download/macosx/"
      echo "   Or install Homebrew first: /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
      exit 1
    fi
  elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux - try package manager
    if command -v apt-get >/dev/null 2>&1; then
      echo "📦 Installing PostgreSQL $REQUIRED_POSTGRES_VERSION via apt..."
      
      # Add PostgreSQL repository for latest version
      sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
      wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
      sudo apt-get update
      sudo apt-get install -y postgresql-$REQUIRED_POSTGRES_VERSION postgresql-contrib
      
      echo "🔄 Starting PostgreSQL service..."
      sudo systemctl start postgresql
      sudo systemctl enable postgresql
      
    elif command -v yum >/dev/null 2>&1; then
      echo "📦 Installing PostgreSQL $REQUIRED_POSTGRES_VERSION via yum..."
      
      # Add PostgreSQL repository
      sudo yum install -y https://download.postgresql.org/pub/repos/yum/reporpms/EL-7-x86_64/pgdg-redhat-repo-latest.noarch.rpm
      sudo yum install -y postgresql$REQUIRED_POSTGRES_VERSION-server postgresql$REQUIRED_POSTGRES_VERSION
      
      echo "🔄 Initializing and starting PostgreSQL service..."
      sudo /usr/pgsql-$REQUIRED_POSTGRES_VERSION/bin/postgresql-$REQUIRED_POSTGRES_VERSION-setup initdb
      sudo systemctl start postgresql-$REQUIRED_POSTGRES_VERSION
      sudo systemctl enable postgresql-$REQUIRED_POSTGRES_VERSION
      
    elif command -v dnf >/dev/null 2>&1; then
      echo "📦 Installing PostgreSQL $REQUIRED_POSTGRES_VERSION via dnf..."
      
      # Add PostgreSQL repository
      sudo dnf install -y https://download.postgresql.org/pub/repos/yum/reporpms/EL-8-x86_64/pgdg-redhat-repo-latest.noarch.rpm
      sudo dnf install -y postgresql$REQUIRED_POSTGRES_VERSION-server postgresql$REQUIRED_POSTGRES_VERSION
      
      echo "🔄 Initializing and starting PostgreSQL service..."
      sudo /usr/pgsql-$REQUIRED_POSTGRES_VERSION/bin/postgresql-$REQUIRED_POSTGRES_VERSION-setup initdb
      sudo systemctl start postgresql-$REQUIRED_POSTGRES_VERSION
      sudo systemctl enable postgresql-$REQUIRED_POSTGRES_VERSION
      
    else
      echo "❌ Unsupported Linux distribution. Please install PostgreSQL $REQUIRED_POSTGRES_VERSION manually."
      echo "   Visit: https://www.postgresql.org/download/linux/"
      exit 1
    fi
  elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "cygwin" ]]; then
    # Windows - provide guidance
    echo "🪟 Windows detected. Please install PostgreSQL $REQUIRED_POSTGRES_VERSION manually:"
    echo "   Visit: https://www.postgresql.org/download/windows/"
    echo "   Or use Windows Package Manager: winget install PostgreSQL.PostgreSQL"
    echo "   Or use Chocolatey: choco install postgresql"
    exit 1
  else
    echo "❌ Unsupported OS: $OSTYPE. Please install PostgreSQL $REQUIRED_POSTGRES_VERSION manually."
    echo "   Visit: https://www.postgresql.org/download/"
    exit 1
  fi
  
  # Verify installation
  if check_postgres_version; then
    echo "✅ PostgreSQL installed successfully"
  else
    echo "❌ Failed to install PostgreSQL $REQUIRED_POSTGRES_VERSION.x. Please install manually."
    exit 1
  fi
}

# Check and install PostgreSQL if needed
echo "🔍 Checking PostgreSQL installation..."
if ! check_postgres_version; then
  echo "🚀 PostgreSQL not found or wrong version, starting installation..."
  install_postgres
else
  echo "✅ PostgreSQL is already properly installed"
  
  # Check if PostgreSQL is in PATH for current session
  if ! command -v psql >/dev/null 2>&1; then
    echo "⚠️  PostgreSQL found but not in PATH for current session"
    echo "🔧 Adding PostgreSQL to shell profile for permanent access..."
    
    SHELL_PROFILE=""
    if [[ -f "$HOME/.zshrc" ]]; then
      SHELL_PROFILE="$HOME/.zshrc"
    elif [[ -f "$HOME/.bash_profile" ]]; then
      SHELL_PROFILE="$HOME/.bash_profile"
    elif [[ -f "$HOME/.bashrc" ]]; then
      SHELL_PROFILE="$HOME/.bashrc"
    else
      SHELL_PROFILE="$HOME/.zshrc"
      touch "$SHELL_PROFILE"
    fi
    
    # Check if PATH is already added to avoid duplicates
    PATH_LINE="export PATH=\"/opt/homebrew/opt/postgresql@$REQUIRED_POSTGRES_VERSION/bin:\$PATH\""
    if ! grep -q "postgresql@$REQUIRED_POSTGRES_VERSION/bin" "$SHELL_PROFILE" 2>/dev/null; then
      echo "" >> "$SHELL_PROFILE"
      echo "# PostgreSQL $REQUIRED_POSTGRES_VERSION - Added by install script" >> "$SHELL_PROFILE"
      echo "$PATH_LINE" >> "$SHELL_PROFILE"
      echo "✅ Added PostgreSQL to $SHELL_PROFILE"
      
      # Export PATH for current session
      export PATH="/opt/homebrew/opt/postgresql@$REQUIRED_POSTGRES_VERSION/bin:$PATH"
      echo "✅ PostgreSQL is now available in current session"
    else
      echo "✅ PostgreSQL PATH already configured in $SHELL_PROFILE"
      # Export PATH for current session
      export PATH="/opt/homebrew/opt/postgresql@$REQUIRED_POSTGRES_VERSION/bin:$PATH"
    fi
  else
    echo "✅ PostgreSQL is accessible in current session"
  fi
fi

if ! command -v pipenv >/dev/null 2>&1; then
  echo "📦 Installing pipenv via pipx..."
  if ! command -v pipx >/dev/null 2>&1; then
    echo "📦 Installing pipx first..."
    if [[ "$OSTYPE" == "darwin"* ]] && command -v brew >/dev/null 2>&1; then
      brew install pipx
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
      if command -v apt-get >/dev/null 2>&1; then
        sudo apt-get install -y pipx
      elif command -v yum >/dev/null 2>&1; then
        sudo yum install -y pipx
      elif command -v dnf >/dev/null 2>&1; then
        sudo dnf install -y pipx
      else
        echo "❌ Cannot install pipx automatically. Please install manually:"
        echo "   pip install --user pipx"
        exit 1
      fi
    else
      echo "❌ Cannot install pipx automatically. Please install manually:"
      echo "   pip install --user pipx"
      exit 1
    fi
  fi
  pipx install pipenv
  export PATH="$HOME/.local/bin:$PATH"
fi

echo "🔧 Setting up project dependencies..."

# Check if virtual environment already exists and has dependencies
if [[ -d ".venv" ]] || [[ -d "$HOME/.local/share/virtualenvs" ]]; then
  echo "📋 Found existing virtual environment, checking if dependencies are set up..."
  
  # Try to import a core dependency to check if everything is working
  if pipenv run python -c "import fastapi" >/dev/null 2>&1; then
    echo "✅ Virtual environment already set up with dependencies"
    echo "🚀 Ready to use! Run: pipenv shell"
    echo ""
    echo "🎉 Installation completed successfully!"
    echo ""
    echo "🚀 Next steps:"
    echo "   1. Set up your environment configuration:"
    echo "      - Copy .env.example to .env: cp .env.example .env"
    echo "      - Edit .env with your actual values (database, secrets, etc.)"
    echo "      - Never commit .env to version control"
    echo "   2. For Docker development:"
    echo "      - Configure database settings in .env"
    echo "      - Run: make up"
    echo "   3. For native development:"
    echo "      - Configure database settings in .env"
    echo "      - Run: pipenv shell && uvicorn app.main:app --reload"
    echo ""
    echo "📖 For detailed environment setup, see: README.md"
echo "🔒 Security: Keep your .env file secure and never share it"
echo ""
echo "💡 PostgreSQL is configured in your shell profile (~/.zshrc)"
echo "   To use PostgreSQL in new terminals, restart your terminal or run: source ~/.zshrc"
    echo ""
    echo "💡 Note: PostgreSQL installation was skipped because virtual environment already exists."
echo "   If you need PostgreSQL, run: brew install postgresql@16"
echo "💡 If PostgreSQL is installed but 'psql' command not found, add to PATH:"
echo "   export PATH=\"/opt/homebrew/opt/postgresql@16/bin:\$PATH\""
echo "💡 To make PostgreSQL available in current session, run:"
echo "   source ~/.zshrc"
    exit 0
  else
    echo "⚠️  Virtual environment exists but dependencies may be missing or outdated"
  fi
fi

# For development, we prefer installing from Pipfile to get latest compatible versions
# Only use Pipfile.lock as a fallback if there are issues
echo "📦 Installing dependencies from Pipfile (development mode)..."
echo "💡 This will install the latest compatible versions of packages"

if ! pipenv install --dev; then
  echo "⚠️  Installation from Pipfile failed, trying with lock file as fallback..."
  
  # Check if Pipfile.lock exists and handle potential conflicts
  if [[ -f "Pipfile.lock" ]]; then
    echo "📋 Found existing Pipfile.lock, checking for compatibility..."
    
    # Detect OS-specific issues
    if [[ "$OSTYPE" == "darwin"* ]]; then
      # macOS: Check for Windows-specific packages
      if grep -q "pywinpty\|winpty" Pipfile.lock 2>/dev/null; then
        echo "⚠️  Detected Windows-specific packages in lock file"
        echo "🔄 Removing lock file to regenerate for macOS..."
        rm Pipfile.lock
      fi
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
      # Linux: Check for macOS-specific packages
      if grep -q "pywinpty\|winpty" Pipfile.lock 2>/dev/null; then
        echo "⚠️  Detected Windows-specific packages in lock file"
        echo "🔄 Removing lock file to regenerate for Linux..."
        rm Pipfile.lock
      fi
    fi
  fi
  
  # Try installing with lock file as fallback
  if ! pipenv install --dev; then
    echo "❌ Failed to install dependencies. Trying minimal installation..."
    
    # Install only essential packages
    pipenv install fastapi uvicorn sqlalchemy psycopg2-binary python-jose passlib python-multipart email-validator python-dotenv bcrypt pydantic pydantic-settings alembic pytest httpx starlette requests pytest-snapshot pytest-cov
    
    if [[ $? -eq 0 ]]; then
      echo "⚠️  Minimal installation completed. Some dev dependencies may be missing."
    else
      echo "❌ Installation failed completely. Please check your system and try again."
      exit 1
    fi
  fi
fi

echo ""
echo "🎉 Installation completed successfully!"
echo ""
echo "🚀 Next steps:"
echo "   1. Set up your environment configuration:"
echo "      - Copy .env.example to .env: cp .env.example .env"
echo "      - Edit .env with your actual values (database, secrets, etc.)"
echo "   2. For Docker development:"
echo "      - Configure database settings in .env"
echo "      - Run: make up"
echo "   3. For native development:"
echo "      - Configure database settings in .env"
echo "      - Run: pipenv shell && uvicorn app.main:app --reload"
echo ""
echo "📖 For detailed environment setup, see: README.md"
