# Docker Setup Guide

This guide will help you install Docker on your system to run the road-test-alert-bc backend.

## Prerequisites

- **macOS**: macOS 10.15 or later
- **Windows**: Windows 10/11 Pro, Enterprise, or Education (64-bit)
- **Linux**: Ubuntu 20.04+, CentOS 7+, or similar

## Installation by Operating System

### macOS

#### Option 1: Docker Desktop (Recommended)
1. Visit [Docker Desktop for Mac](https://docs.docker.com/desktop/install/mac-install/)
2. Download the appropriate version for your Mac (Intel or Apple Silicon)
3. Double-click the downloaded `.dmg` file
4. Drag Docker to Applications folder
5. Open Docker from Applications
6. Follow the setup wizard

#### Option 2: Homebrew
```bash
brew install --cask docker
```

### Windows

#### Docker Desktop (Recommended)
1. Visit [Docker Desktop for Windows](https://docs.docker.com/desktop/install/windows-install/)
2. Download Docker Desktop for Windows
3. Run the installer
4. Enable WSL 2 if prompted
5. Restart your computer
6. Start Docker Desktop

#### WSL 2 Backend (Alternative)
```bash
# Install WSL 2
wsl --install

# Install Docker in WSL 2
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
```

### Linux

#### Ubuntu/Debian
```bash
# Update package index
sudo apt-get update

# Install prerequisites
sudo apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg \
    lsb-release

# Add Docker's official GPG key
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# Add Docker repository
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker Engine
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

# Add user to docker group
sudo usermod -aG docker $USER

# Start Docker service
sudo systemctl start docker
sudo systemctl enable docker
```

#### CentOS/RHEL/Fedora
```bash
# Install prerequisites
sudo yum install -y yum-utils

# Add Docker repository
sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo

# Install Docker Engine
sudo yum install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

# Start Docker service
sudo systemctl start docker
sudo systemctl enable docker

# Add user to docker group
sudo usermod -aG docker $USER
```

## Verify Installation

After installation, verify Docker is working:

```bash
# Check Docker version
docker --version

# Check Docker Compose version
docker compose version

# Run hello-world container
docker run hello-world
```

## Post-Installation Steps

### 1. Logout and Login Again
After adding your user to the docker group, logout and login again for the changes to take effect.

### 2. Test Docker Compose
```bash
# Test with a simple compose file
echo 'version: "3.9"
services:
  hello:
    image: hello-world' > test-compose.yml

docker compose -f test-compose.yml up

# Clean up
docker compose -f test-compose.yml down
rm test-compose.yml
```

## Troubleshooting

### Common Issues

#### Permission Denied
```bash
# Add user to docker group (Linux/macOS)
sudo usermod -aG docker $USER

# Logout and login again, or run:
newgrp docker
```

#### Docker Desktop Not Starting (macOS/Windows)
- Check system requirements
- Ensure virtualization is enabled in BIOS
- Try restarting Docker Desktop
- Check system logs for errors

#### Port Already in Use
```bash
# Check what's using port 8000
lsof -i :8000

# Kill the process if needed
kill -9 <PID>
```

### Getting Help

- [Docker Documentation](https://docs.docker.com/)
- [Docker Community Forums](https://forums.docker.com/)
- [GitHub Issues](https://github.com/docker/docker-ce/issues)

## Alternative: Use Without Docker

If you can't install Docker, you can still develop using the native path:

```bash
# Install Python 3.12 and dependencies
bash scripts/install.sh

# Activate virtual environment
pipenv shell

# Run the application
uvicorn app.main:app --reload
```

Note: You'll need to install and configure PostgreSQL separately for the database.
