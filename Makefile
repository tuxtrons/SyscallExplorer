.PHONY: install install-dev test format lint clean build run-backend run-frontend dev help

# Default target
help:
	@echo "SystemCallExplorer Development Commands"
	@echo "======================================"
	@echo "install       - Install production dependencies"
	@echo "install-dev   - Install development dependencies"
	@echo "test          - Run tests"
	@echo "format        - Format code"
	@echo "lint          - Run linters"
	@echo "clean         - Clean build artifacts"
	@echo "build         - Build for production"
	@echo "run-backend   - Run backend development server"
	@echo "run-frontend  - Run frontend development server"
	@echo "dev           - Run both backend and frontend in development"

# Installation targets
install:
	cd backend && pip install -r requirements.txt
	cd frontend && npm install

install-dev: install
	cd backend && pip install -r requirements-dev.txt
	cd frontend && npm install --include=dev

# Development targets
run-backend:
	cd backend && python main.py

run-frontend:
	cd frontend && npm run dev

dev:
	@echo "Starting SystemCallExplorer development servers..."
	@echo "Backend: http://localhost:8000"
	@echo "Frontend: http://localhost:5173"
	@echo "API Docs: http://localhost:8000/docs"
	cd backend && python main.py &
	cd frontend && npm run dev

# Testing and quality
test:
	cd backend && python -m pytest tests/
	cd frontend && npm test

format:
	cd backend && black . && isort .
	cd frontend && npm run format

lint:
	cd backend && flake8 . && mypy .
	cd frontend && npm run lint

# Build and deployment
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	cd frontend && rm -rf dist/ node_modules/.cache/

build: clean
	cd frontend && npm run build

# Docker targets (for future use)
docker-build:
	docker build -t systemcall-explorer .

docker-run:
	docker run -p 8000:8000 -p 5173:5173 systemcall-explorer