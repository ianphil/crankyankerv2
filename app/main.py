import json
import os
from fastapi import FastAPI, HTTPException
from pathlib import Path
from app.training_plan.plan import Plan
app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI + uv!"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}

@app.get("/plans/{user_id}")
def get_plan(user_id: str):
    """Get training plans for a user from data folder"""
    data_dir = Path("data")
    user_plans_dir = data_dir / user_id / "training_plans"
    
    if not user_plans_dir.exists():
        raise HTTPException(status_code=404, detail="User not found")
    
    plans = []
    for json_file in user_plans_dir.glob("*.json"):
        try:
            with open(json_file, 'r') as f:
                plan_data = json.load(f)
                plans.append(plan_data)
        except (json.JSONDecodeError, IOError):
            continue
    
    if not plans:
        raise HTTPException(status_code=404, detail="No plans found for user")
    
    return {"user_id": user_id, "plans": plans}