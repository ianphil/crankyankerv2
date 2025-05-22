import json
import os
from datetime import datetime
from pathlib import Path
from typing import List
from uuid import uuid4
from pydantic import BaseModel, Field

class Workout(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()), description="Unique identifier for the workout")
    name: str = Field(..., description="Name of the workout", json_schema_extra={"example": "Morning Run"})
    description: str = Field(..., description="Detailed description of the workout", json_schema_extra={"example": "Easy-paced 30-minute run to build aerobic base"})
    duration: int = Field(..., description="Duration of the workout in minutes", gt=0, json_schema_extra={"example": 30})
    intensity: str = Field(..., description="Intensity level of the workout", json_schema_extra={"example": "Easy"})
    
class Block(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()), description="Unique identifier for the training block")
    name: str = Field(..., description="Name of the training block", json_schema_extra={"example": "Base Building Week 1"})
    start_date: datetime = Field(..., description="Start date of the training block", json_schema_extra={"example": "2024-01-01T00:00:00"})
    end_date: datetime = Field(..., description="End date of the training block", json_schema_extra={"example": "2024-01-07T23:59:59"})
    workouts: List[Workout] = Field(..., description="List of workouts in this training block")

class Phase(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()), description="Unique identifier for the training phase")
    name: str = Field(..., description="Name of the training phase", json_schema_extra={"example": "Base Building"})
    description: str = Field(..., description="Description of the training phase", json_schema_extra={"example": "Foundational aerobic development phase"})
    start_date: datetime = Field(..., description="Start date of the training phase", json_schema_extra={"example": "2024-01-01T00:00:00"})
    end_date: datetime = Field(..., description="End date of the training phase", json_schema_extra={"example": "2024-02-29T23:59:59"})
    blocks: List[Block] = Field(..., description="List of training blocks in this phase")

class Plan(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()), description="Unique identifier for the training plan")
    athlete_id: str = Field(..., description="Unique identifier of the athlete", json_schema_extra={"example": "athlete_123"})
    target_date: datetime = Field(..., description="Target completion date for the training plan", json_schema_extra={"example": "2024-06-01T00:00:00"})
    name: str = Field(..., description="Name of the training plan", json_schema_extra={"example": "Marathon Training Plan"})
    description: str = Field(..., description="Detailed description of the training plan", json_schema_extra={"example": "16-week marathon training plan for sub-3:30 goal"})
    phases: List[Phase] = Field(..., description="List of training phases in the plan")


def save_training_plan(plan: Plan, user_id: str, data_dir: str = "data") -> str:
    """
    Save a training plan to disk organized by user ID.
    
    Args:
        plan: The training plan to save
        user_id: The user ID to organize the file under
        data_dir: Base directory for data storage (default: "data")
    
    Returns:
        str: Path to the saved file
    """
    # Create directory structure
    user_dir = Path(data_dir) / user_id / "training_plans"
    user_dir.mkdir(parents=True, exist_ok=True)
    
    # Create filename with plan ID and sanitized name
    safe_name = "".join(c for c in plan.name if c.isalnum() or c in (' ', '-', '_')).strip()
    safe_name = safe_name.replace(' ', '_')
    filename = f"{plan.id}_{safe_name}.json"
    file_path = user_dir / filename
    
    # Save plan as JSON
    with open(file_path, 'w') as f:
        json.dump(plan.model_dump(mode='json'), f, indent=2, default=str)
    
    return str(file_path)