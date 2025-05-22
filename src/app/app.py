import json
import os
from fastapi import FastAPI, HTTPException
from pathlib import Path
from src.app.training_plan.plan import Plan
app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI + uv!"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}

@app.get("/plans/{plan_id}")
def get_plan(plan_id: str):
    """Get a training plan by ID from data folder"""
    data_dir = Path("data")
    
    # Find the JSON file with the given plan_id
    for user_dir in data_dir.glob("*/training_plans"):
        for json_file in user_dir.glob("*.json"):
            try:
                with open(json_file, 'r') as f:
                    plan_data = json.load(f)
                    if plan_data.get("id") == plan_id:
                        return plan_data
            except (json.JSONDecodeError, IOError):
                continue
    
    raise HTTPException(status_code=404, detail="Plan not found")