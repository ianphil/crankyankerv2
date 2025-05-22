import json
import os
from datetime import datetime
from fastapi import FastAPI, HTTPException
from pathlib import Path
from app.training_plan.plan import Plan
from app.models.responses import PlanListResponse, ItemResponse, HealthResponse, ErrorResponse
from app.core.config import OPENAPI_TAGS, API_TITLE, API_DESCRIPTION, API_VERSION

app = FastAPI(
    title=API_TITLE,
    description=API_DESCRIPTION,
    version=API_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    openapi_tags=OPENAPI_TAGS
)

@app.get(
    "/",
    response_model=dict,
    tags=["health"],
    summary="Root endpoint",
    description="Welcome message and basic API information"
)
def read_root():
    """
    Root endpoint that returns a welcome message.
    
    This endpoint can be used to verify that the API is running.
    """
    return {"message": "Hello from FastAPI + uv!", "api": "Training Plan API", "version": API_VERSION}

@app.get(
    "/items/{item_id}",
    response_model=ItemResponse,
    tags=["items"],
    summary="Get item by ID",
    description="Retrieve a specific item by its ID with optional query parameter"
)
def read_item(item_id: int, q: str | None = None):
    """
    Retrieve an item by its ID.
    
    - **item_id**: The ID of the item to retrieve
    - **q**: Optional query parameter for filtering or search
    
    Returns the item data along with any query parameters.
    """
    return ItemResponse(item_id=item_id, q=q)

@app.get(
    "/plans/{user_id}",
    response_model=PlanListResponse,
    tags=["plans"],
    summary="Get training plans for user",
    description="Retrieve all training plans for a specific user",
    responses={
        200: {
            "description": "Successfully retrieved training plans",
            "model": PlanListResponse
        },
        404: {
            "description": "User not found or no plans available",
            "model": ErrorResponse
        }
    }
)
def get_plan(user_id: str):
    """
    Retrieve all training plans for a specific user.
    
    This endpoint searches the data directory for training plans associated 
    with the specified user ID and returns them as a list.
    
    - **user_id**: Unique identifier for the user
    
    Returns:
    - List of training plans for the user
    - Total count of plans found
    - Success message
    
    Raises:
    - 404: If user directory doesn't exist or no plans are found
    """
    data_dir = Path("data")
    user_plans_dir = data_dir / user_id / "training_plans"
    
    if not user_plans_dir.exists():
        raise HTTPException(
            status_code=404, 
            detail=f"User '{user_id}' not found"
        )
    
    plans = []
    for json_file in user_plans_dir.glob("*.json"):
        try:
            with open(json_file, 'r') as f:
                plan_data = json.load(f)
                plans.append(Plan(**plan_data))
        except (json.JSONDecodeError, IOError) as e:
            continue
    
    if not plans:
        raise HTTPException(
            status_code=404, 
            detail=f"No training plans found for user '{user_id}'"
        )
    
    return PlanListResponse(
        user_id=user_id,
        plans=plans,
        count=len(plans),
        message=f"Successfully retrieved {len(plans)} training plan(s) for user '{user_id}'"
    )


@app.get(
    "/health",
    response_model=HealthResponse,
    tags=["health"],
    summary="Health check",
    description="Check the health status of the API service"
)
def health_check():
    """
    Health check endpoint to verify API service status.
    
    Returns current service status, timestamp, and API version.
    This endpoint can be used by monitoring systems and load balancers.
    """
    return HealthResponse(
        status="healthy",
        timestamp=datetime.utcnow().isoformat() + "Z",
        version=API_VERSION
    )