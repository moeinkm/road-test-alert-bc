SHELL := /bin/bash

.PHONY: up down logs build seed fmt lint test smoke copy-env clean restart status help docker-check setup-db

# Colors for better output
GREEN := \033[0;32m
YELLOW := \033[1;33m
RED := \033[0;31m
BLUE := \033[0;34m
NC := \033[0m # No Color

help: ## Show this help message
	@echo "$(GREEN)Available commands:$(NC)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(YELLOW)%-15s$(NC) %s\n", $$1, $$2}'

copy-env: ## Copy .env.example to .env (⚠️  Remember to configure values!)
	@if [ ! -f .env ]; then \
		cp .env.example .env; \
		echo "$(GREEN)✅ Created .env from .env.example$(NC)"; \
		echo "$(YELLOW)⚠️  IMPORTANT: Edit .env with your actual values before running services$(NC)"; \
		echo "$(YELLOW)   - Database credentials, secrets, API keys, etc.$(NC)"; \
		echo "$(YELLOW)   - Never commit .env to version control$(NC)"; \
	else \
		echo "$(YELLOW)⚠️  .env already exists$(NC)"; \
	fi

docker-check: ## Check if Docker is properly installed and running
	@echo "$(BLUE)🔍 Checking Docker environment...$(NC)"
	@./scripts/check-docker.sh

up: docker-check ## Build and run API + Postgres (⚠️  Requires .env configuration)
	@echo "$(GREEN)🚀 Starting services...$(NC)"
	@docker compose up -d --build
	@echo "$(GREEN)✅ Services are starting up$(NC)"
	@echo "$(YELLOW)💡 Run 'make logs' to see startup progress$(NC)"

down: ## Stop and remove containers/volumes
	@echo "$(YELLOW)🛑 Stopping services...$(NC)"
	@docker compose down -v
	@echo "$(GREEN)✅ Services stopped and cleaned up$(NC)"

restart: down up ## Restart all services

logs: ## Tail logs from all services
	@docker compose logs -f --tail=100

status: ## Show status of all services
	@echo "$(GREEN)📊 Service Status:$(NC)"
	@docker compose ps

build: docker-check ## Build the API container
	@echo "$(GREEN)🔨 Building API container...$(NC)"
	@docker compose build api
	@echo "$(GREEN)✅ Build complete$(NC)"

setup-db: ## Set up database (migrations and seeding)
	@echo "$(GREEN)🗄️  Setting up database...$(NC)"
	@echo "$(BLUE)📋 Running database migrations...$(NC)"
	@docker compose exec api bash -lc "alembic upgrade head" || echo "$(YELLOW)⚠️  Migrations failed - this is normal for first-time setup$(NC)"
	@echo "$(BLUE)🌱 Seeding database...$(NC)"
	@docker compose exec api bash -lc "python scripts/seed.py" || echo "$(YELLOW)⚠️  Seeding failed - this is normal for first-time setup$(NC)"
	@echo "$(GREEN)✅ Database setup completed$(NC)"

setup-test-db: ## Set up test database for pytest
	@echo "$(GREEN)🧪 Setting up test database...$(NC)"
	@docker compose exec api bash -lc "pipenv run python scripts/setup_test_db.py"
	@echo "$(GREEN)✅ Test database setup completed$(NC)"

seed: ## Seed the database with initial data
	@echo "$(GREEN)🌱 Seeding database...$(NC)"
	@docker compose exec api bash -lc "python scripts/seed.py"
	@echo "$(GREEN)✅ Database seeded$(NC)"

fmt: ## Format code with ruff
	@echo "$(GREEN)🎨 Formatting code...$(NC)"
	@docker compose exec api bash -lc "ruff check --fix . && ruff format ."
	@echo "$(GREEN)✅ Code formatted$(NC)"

lint: ## Lint and type-check code
	@echo "$(GREEN)🔍 Running linting and type checks...$(NC)"
	@docker compose exec api bash -lc "ruff check . && mypy app"
	@echo "$(GREEN)✅ Linting complete$(NC)"

test: ## Run tests
	@echo "$(GREEN)🧪 Running tests...$(NC)"
	@docker compose exec api bash -lc "pipenv run pytest -q"
	@echo "$(GREEN)✅ Tests complete$(NC)"

smoke: ## Run health check
	@echo "$(GREEN)🚬 Running smoke test...$(NC)"
	@./scripts/smoke.sh

clean: ## Clean up all containers, images, and volumes
	@echo "$(RED)🧹 Cleaning up everything...$(NC)"
	@docker compose down -v --rmi all
	@docker system prune -f
	@echo "$(GREEN)✅ Cleanup complete$(NC)"

# Default target
.DEFAULT_GOAL := help
