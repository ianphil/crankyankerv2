from typing import List, Optional, Any
from pydantic import BaseModel, Field
from app.training_plan.plan import Plan


class ErrorResponse(BaseModel):
    """Standardized error response model"""
    detail: str = Field(..., description="Error message", json_schema_extra={"example": "User not found"})
    status_code: int = Field(..., description="HTTP status code", json_schema_extra={"example": 404})


class HealthResponse(BaseModel):
    """Health check response model"""
    status: str = Field(..., description="Service status", json_schema_extra={"example": "healthy"})
    timestamp: str = Field(..., description="Response timestamp", json_schema_extra={"example": "2024-01-01T12:00:00Z"})
    version: str = Field(..., description="API version", json_schema_extra={"example": "1.0.0"})


class PlanResponse(BaseModel):
    """Single training plan response"""
    user_id: str = Field(..., description="User identifier", json_schema_extra={"example": "sample_user_123"})
    plan: Plan = Field(..., description="Training plan data")
    message: str = Field(..., description="Response message", json_schema_extra={"example": "Plan retrieved successfully"})


class PlanListResponse(BaseModel):
    """Multiple training plans response"""
    user_id: str = Field(..., description="User identifier", json_schema_extra={"example": "sample_user_123"})
    plans: List[Plan] = Field(..., description="List of training plans")
    count: int = Field(..., description="Number of plans returned", json_schema_extra={"example": 2})
    message: str = Field(..., description="Response message", json_schema_extra={"example": "Plans retrieved successfully"})
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "user_id": "sample_user_123",
                "plans": [
                    {
                        "id": "plan_456",
                        "athlete_id": "athlete_123",
                        "target_date": "2024-06-01T00:00:00",
                        "name": "Marathon Training Plan",
                        "description": "16-week marathon training plan for sub-3:30 goal",
                        "phases": []
                    }
                ],
                "count": 1,
                "message": "Successfully retrieved 1 training plan(s) for user 'sample_user_123'"
            }
        }
    }


class ItemResponse(BaseModel):
    """Generic item response (legacy)"""
    item_id: int = Field(..., description="Item identifier", json_schema_extra={"example": 123})
    q: Optional[str] = Field(None, description="Optional query parameter", json_schema_extra={"example": "test"})