# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a FastAPI-based training plan application using `uv` for Python dependency management. The project models athletic training plans with hierarchical structures: Plans contain Phases, Phases contain Blocks, and Blocks contain Workouts.

## Key Commands

- **Run tests**: `uv run pytest`
- **Debug/Development**: Use F5 (configured for debugging)
- **Run development server**: `uv run uvicorn app.app:app --reload` (from src/app directory)
- **Production server**: `uv run gunicorn --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000 app:app`

## Architecture

### Core Models (src/app/training_plan/plan.py)
The application uses Pydantic models in a hierarchical structure:
- `Plan`: Top-level training plan with athlete_id, target_date, and phases
- `Phase`: Training phase with start/end dates and blocks  
- `Block`: Training block containing multiple workouts
- `Workout`: Individual workout with name, description, duration, and intensity

Each model auto-generates UUIDs using `uuid4()` and uses Pydantic for validation.

### FastAPI Application (src/app/app.py)
Basic FastAPI setup with root endpoint and parameterized item endpoint. The app is designed to be extended with training plan endpoints.

## Test Configuration

Tests are located in `src/tests/` with pytest configured to:
- Add `src/` to PYTHONPATH automatically
- Run with verbose output (`-v`)
- Use the test file structure that mirrors the app structure

## Docker Support

The application includes a multi-stage Docker build using the official `uv` Alpine image, optimized for layer caching and production deployment with gunicorn + uvicorn workers.