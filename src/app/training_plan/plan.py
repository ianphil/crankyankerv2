from datetime import datetime
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