import json
import os
from datetime import datetime
from pathlib import Path
from typing import List
from uuid import uuid4
from pydantic import BaseModel, Field

class Workout(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    name: str
    description: str
    duration: int  # in minutes
    intensity: str
    
class Block(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    name: str
    start_date: datetime
    end_date: datetime
    workouts: List[Workout]

class Phase(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    name: str
    description: str
    start_date: datetime
    end_date: datetime
    blocks: List[Block]

class Plan(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    athlete_id: str
    target_date: datetime
    name: str
    description: str
    phases: List[Phase]


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