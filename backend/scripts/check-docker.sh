#!/usr/bin/env bash
set -euo pipefail

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🔍 Checking Docker installation and status...${NC}"

# Check if Docker is installed
if ! command -v docker >/dev/null 2>&1; then
    echo -e "${RED}❌ Docker is not installed${NC}"
    echo -e "${YELLOW}💡 Please install Docker first:${NC}"
    echo -e "   📖 See: docs/docker-setup.md"
    echo -e "   🌐 Or visit: https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if Docker Compose is available
if ! command -v docker compose >/dev/null 2>&1; then
    echo -e "${RED}❌ Docker Compose is not available${NC}"
    echo -e "${YELLOW}💡 Please install Docker Compose:${NC}"
    echo -e "   📖 See: docs/docker-setup.md"
    exit 1
fi

# Check Docker version
DOCKER_VERSION=$(docker --version)
echo -e "${GREEN}✅ Docker found: ${DOCKER_VERSION}${NC}"

# Check Docker Compose version
COMPOSE_VERSION=$(docker compose version)
echo -e "${GREEN}✅ Docker Compose found: ${COMPOSE_VERSION}${NC}"

# Check if Docker daemon is running
if ! docker info >/dev/null 2>&1; then
    echo -e "${RED}❌ Docker daemon is not running${NC}"
    echo -e "${YELLOW}💡 Please start Docker:${NC}"
    
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo -e "   🍎 On macOS: Open Docker Desktop from Applications"
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo -e "   🐧 On Linux: sudo systemctl start docker"
    else
        echo -e "   💻 Start Docker Desktop or Docker service"
    fi
    exit 1
fi

# Check Docker daemon info
echo -e "${GREEN}✅ Docker daemon is running${NC}"

# Test Docker functionality
echo -e "${BLUE}🧪 Testing Docker functionality...${NC}"

if docker run --rm hello-world >/dev/null 2>&1; then
    echo -e "${GREEN}✅ Docker can run containers${NC}"
else
    echo -e "${RED}❌ Docker cannot run containers${NC}"
    echo -e "${YELLOW}💡 This might be a permission issue${NC}"
    echo -e "   🔧 Try: sudo usermod -aG docker \$USER"
    echo -e "   🔄 Then logout and login again"
    exit 1
fi

# Check available disk space
DISK_SPACE=$(df . | awk 'NR==2 {print $4}')
DISK_SPACE_GB=$((DISK_SPACE / 1024 / 1024))

if [ "$DISK_SPACE_GB" -gt 5 ]; then
    echo -e "${GREEN}✅ Sufficient disk space: ${DISK_SPACE_GB}GB available${NC}"
else
    echo -e "${YELLOW}⚠️  Low disk space: ${DISK_SPACE_GB}GB available${NC}"
    echo -e "   💡 Docker needs at least 5GB for comfortable development"
fi

# Check Docker Compose functionality
echo -e "${BLUE}🧪 Testing Docker Compose...${NC}"

# Create a temporary test compose file
cat > /tmp/test-compose.yml << 'EOF'
version: "3.9"
services:
  hello:
    image: hello-world
EOF

if docker compose -f /tmp/test-compose.yml up >/dev/null 2>&1; then
    echo -e "${GREEN}✅ Docker Compose is working${NC}"
else
    echo -e "${RED}❌ Docker Compose test failed${NC}"
    exit 1
fi

# Clean up test file
rm -f /tmp/test-compose.yml

echo -e "${GREEN}🎉 Docker environment is ready!${NC}"
echo -e "${BLUE}💡 You can now run: make up${NC}"
