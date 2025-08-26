# road-test-alert-bc Backend

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.12** (will be installed automatically by `install.sh`/`install.bat`)
- **Docker & Docker Compose** (see [Docker Setup Guide](docs/docker-setup.md))

**Note**: Our installation scripts will automatically install Python 3.12 if it's not present on your system.

## Quickstart

### Option 1: Docker (Recommended)
```bash
git clone <repo>
cd road-test-alert-bc/backend
make up
make setup-db  # Runs migrations and seeds database
make setup-test-db # Create test db to enable tests to run successfuly
make smoke
```

### Option 2: Native Development

#### macOS/Linux
```bash
git clone <repo>
cd road-test-alert-bc/backend
bash scripts/install.sh
# Follow the setup instructions provided by the script
# Configure your environment in .env
# Set up your database (PostgreSQL must be running)
pipenv shell
pipenv run python scripts/setup_db.py  # Create database and user
pipenv run python scripts/setup_test_db.py  # Create test db to enable tests to run successfuly
pipenv run alembic upgrade head  # Run migrations
pipenv run python scripts/seed.py  # Seed database
uvicorn app.main:app --reload
```

#### Windows
```cmd
git clone <repo>
cd road-test-alert-bc\backend
scripts\install.bat
# Follow the setup instructions provided by the script
# Configure your environment in .env
# Set up your database (PostgreSQL must be running)
pipenv run python scripts/setup_db.py  # Create database and user
pipenv run python scripts/setup_test_db.py  # Create test database for pytest
pipenv run alembic upgrade head  # Run migrations
pipenv run python scripts/seed.py  # Seed database
pipenv shell
uvicorn app.main:app --reload
```

- API: [http://localhost:8000](http://localhost:8000)
- Health: `GET /api/v1/health` → `{"status":"ok"}`
- Down: `make down`

**Note**: Docker uses port 8000 by default. For native development, use port 8001 to avoid conflicts: `uvicorn app.main:app --reload --port 8001`

## Database Setup

### Docker Development (Automatic)
Docker automatically handles database setup:
- ✅ Creates database and user
- ✅ Runs migrations
- ✅ Seeds initial data
- ✅ Manages environment variables

### Native Development (Manual)
For native development, you need to set up the database manually:

```bash
# 1. Create database and user
pipenv run python scripts/setup_db.py

# 2. Run migrations to create tables
pipenv run alembic upgrade head

# 3. Seed with initial data (optional)
pipenv run python scripts/seed.py

# 4. Create test database for pytest (optional)
pipenv run python scripts/setup_test_db.py
```

**Note**: The `setup_db.py` script reads your `.env` file and creates the database and user specified in your environment variables.

### Docker vs Native Development Database Configuration

**Important**: Docker and native development require different database hostnames in your `.env` file.

### Troubleshooting Database Issues

**Common Issues:**

1. **PostgreSQL not running**
   ```bash
   # macOS
   brew services start postgresql@16
   
   # Linux
   sudo systemctl start postgresql
   
   # Windows
   # Start PostgreSQL service from Services
   ```

2. **Permission denied**
   ```bash
   # Make sure PostgreSQL is accessible
   psql postgres -c "\du"
   ```

3. **Database already exists**
   ```bash
   # The setup script will handle this gracefully
   pipenv run python scripts/setup_db.py
   ```

4. **Environment variables not loaded**
   ```bash
   # Make sure .env file exists and has correct values
   cat .env | grep DATABASE
   ```

## Docker Setup

If you don't have Docker installed, follow our comprehensive setup guide:

```bash
# Check if Docker is ready
make docker-check

# If Docker is not ready, see:
open docs/docker-setup.md
```

The setup guide covers:
- **macOS**: Docker Desktop or Homebrew installation
- **Windows**: Docker Desktop with WSL 2 support
- **Linux**: Package manager installation for Ubuntu/Debian/CentOS
- **Troubleshooting**: Common issues and solutions

## Cross-Platform Installation

Our installation scripts automatically handle different operating systems:

### **macOS**
- **Uses Homebrew** if available for Python 3.12 installation
- Provides clear guidance if Homebrew is not installed
- Handles both Intel and Apple Silicon Macs
- Automatically detects and resolves PATH issues
- Handles dependency conflicts intelligently

### **Linux**
- Supports Ubuntu/Debian (apt), CentOS/RHEL (yum), Fedora (dnf)
- Installs Python 3.12 via package manager
- Creates necessary symlinks automatically
- Handles dependency conflicts and fallbacks

### **Windows**
- Dedicated `install.bat` script
- **Automatically installs Python 3.12** via winget or Chocolatey
- Falls back to manual installation instructions if needed
- Handles Windows-specific dependency issues
- Provides clear error messages and solutions

### **PostgreSQL for Native Development**
For native development, you'll need to install PostgreSQL separately:

#### **Option 1: Local Installation**
- **macOS**: `brew install postgresql` or download from [postgresql.org](https://www.postgresql.org/download/macosx/)
- **Linux**: `sudo apt install postgresql` (Ubuntu/Debian) or equivalent for your distribution
- **Windows**: Download from [postgresql.org](https://www.postgresql.org/download/windows/)

#### **Option 2: Docker Database Only**
```bash
# Run PostgreSQL in Docker (recommended for development)
docker run --name postgres-dev \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=password \
  -e POSTGRES_DB=road_test_alert \
  -p 5432:5432 \
  -d postgres:15

# Configure .env with:
# DATABASE_URL=postgresql://postgres:password@localhost:5432/road_test_alert
```

#### **Option 3: Cloud Database**
- **AWS RDS**: Managed PostgreSQL service
- **Google Cloud SQL**: Managed PostgreSQL service
- **Supabase**: Open source Firebase alternative
- **Railway**: Simple PostgreSQL hosting

**Note**: For production, always use managed database services or properly configured PostgreSQL instances.

### **Smart Dependency Resolution**
- Automatically detects OS-specific package conflicts
- Removes incompatible lock files when needed
- Falls back to minimal installation if full install fails
- Handles cross-platform package compatibility
- **Guided setup** - provides clear instructions for missing dependencies

### **Development vs Production Dependencies**

#### **Development (Local)**
- **Installs from `Pipfile`** - Gets latest compatible versions
- **Flexible versions** - Allows dependency updates and testing
- **Fast iteration** - Developers can test new package versions

#### **Production (Docker)**
- **Installs from `Pipfile.lock`** - Ensures reproducible builds
- **Fixed versions** - Guarantees deployment consistency
- **Security** - Prevents unexpected dependency changes

## Development Commands

### Core Operations
- `make up` — Build and run API + Postgres with health checks
- `make down` — Stop and remove containers/volumes
- `make restart` — Restart all services
- `make status` — Show service status
- `make logs` — Tail logs from all services

### Development Workflow
- `make setup-db` — Set up database (migrations + seeding)
- `make seed` — Seed DB with initial data (idempotent)
- `make smoke` — Health check with detailed output
- `make fmt` — Format code with ruff
- `make lint` — Lint and type-check code
- `make test` — Run tests
- `make build` — Build API container only

### Maintenance
- `make clean` — Clean up all containers, images, and volumes
- `make help` — Show all available commands
- `make docker-check` — Verify Docker installation and status



## Environment Variables

### Environment Setup
**⚠️  Important**: Before running any services, you must configure your environment:

1. **Copy the example file**: `cp .env.example .env`
2. **Edit `.env`** with your actual values:
   - Database credentials (username, password, database name)
   - API keys and secrets
   - Email configuration
   - ICBC URLs and credentials
3. **Never commit `.env`** to version control
4. **Keep `.env` secure** - it contains sensitive information

**Note**: The installation scripts will provide specific guidance for environment setup after completion.

### Database Configuration
- `DB_TIMEOUT` - Database connection timeout (default: 30s)
- `SMOKE_TIMEOUT` - Health check timeout (default: 10s)

### Service Configuration
- `APP_PORT` - API service port (default: 8000)
- `DATABASE_URL` - PostgreSQL connection string
- `DATABASE_USER` - Database username
- `DATABASE_PASSWORD` - Database password
- `DATABASE_NAME` - Database name

## Docker Features

### Security
- Non-root user execution
- Health checks for both API and database
- Optimized layer caching
- Comprehensive `.dockerignore`

### Development Experience
- Live code reloading with volume mounts
- Health check dependencies
- Configurable timeouts
- Detailed logging and error messages

### Build Strategy
- **Local builds**: Use `Pipfile` for latest dependencies
- **Production builds**: Use `Pipfile.lock` for reproducibility
- **Environment-aware**: Automatically chooses the right approach

## CI
- See `.github/workflows/ci.yml`

---

- **Environment Setup**: Copy `.env.example` to `.env` and configure with your actual values
- No secrets in git. Use `.env` for local/dev, CI secrets for CI
- All scripts include proper error handling and user feedback
- Docker setup includes health checks and proper service orchestration
- **New users**: Start with `make docker-check` to verify your environment
- **Cross-platform**: Use `install.sh` (macOS/Linux) or `install.bat` (Windows)
- **Guided setup**: Installation scripts install Python 3.12 if available tools are present, otherwise provide clear guidance
- **Separation of concerns**: `install.sh`/`install.bat` handle setup, `make setup-db` handles Docker database operations
- **Dependency strategy**: Development uses `Pipfile` (latest), production uses `Pipfile.lock` (fixed)
- **Environment configuration**: Always configure `.env` before running services
- **Database setup**: Use `make setup-db` for Docker, direct commands for native development
