from typing import List

# OpenAPI configuration
OPENAPI_TAGS = [
    {
        "name": "plans",
        "description": "Training plan operations - create, retrieve, and manage athletic training plans",
    },
    {
        "name": "health",
        "description": "Health check endpoints - monitor API service status",
    },
    {
        "name": "items",
        "description": "Generic item operations (legacy endpoints)",
    },
]

# API metadata
API_TITLE = "Training Plan API"
API_DESCRIPTION = """
A comprehensive API for managing athletic training plans with hierarchical structure.

## Features

* **Hierarchical Structure**: Plans → Phases → Blocks → Workouts
* **User Organization**: Plans organized by user ID
* **JSON Storage**: File-based storage in structured directories
* **Validation**: Pydantic models with comprehensive validation

## Training Plan Structure

1. **Plan**: Top-level training plan with target date and athlete information
2. **Phase**: Training phases (e.g., Base Building, Peak, Taper)
3. **Block**: Weekly or multi-day training blocks
4. **Workout**: Individual training sessions with duration and intensity

## Data Storage

Plans are stored in the following structure:
```
data/
├── {user_id}/
│   └── training_plans/
│       ├── {plan_id}_{plan_name}.json
│       └── ...
```
"""
API_VERSION = "1.0.0"