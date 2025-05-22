import pytest
from datetime import datetime, timedelta
from fastapi.testclient import TestClient
from app.training_plan.plan import Plan, Phase, Block, Workout
from app.main import app

# Make sure this file is loaded by pytest
pytestmark = pytest.mark.usefixtures()

def test_create_sample_plan():
    # Create sample workouts
    easy_run = Workout(
        name="Easy Run",
        description="Zone 2 endurance run",
        duration=45,
        intensity="low"
    )
    
    tempo_run = Workout(
        name="Tempo Run",
        description="Zone 4 tempo intervals",
        duration=60,
        intensity="high"
    )

    # Create a training block
    base_block = Block(
        name="Base Building",
        start_date=datetime.now(),
        end_date=datetime.now() + timedelta(weeks=2),
        workouts=[easy_run, tempo_run]
    )

    # Create a phase
    base_phase = Phase(
        name="Base Phase",
        description="Building aerobic base and introducing intensity",
        start_date=datetime.now(),
        end_date=datetime.now() + timedelta(weeks=4),
        blocks=[base_block]
    )

    # Create the complete training plan
    training_plan = Plan(
        athlete_id="12345",
        target_date=datetime.now() + timedelta(weeks=12),
        name="Marathon Training Plan",
        description="16-week marathon training plan for intermediate runners",
        phases=[base_phase]
    )

    # Assert that the plan was created with all required components
    assert training_plan.name == "Marathon Training Plan"
    assert len(training_plan.phases) == 1
    assert len(training_plan.phases[0].blocks) == 1
    assert len(training_plan.phases[0].blocks[0].workouts) == 2
    assert training_plan.phases[0].blocks[0].workouts[0].name == "Easy Run"
    assert training_plan.phases[0].blocks[0].workouts[1].name == "Tempo Run"


client = TestClient(app)

def test_get_plan_user_not_found():
    """Test that getting plans for a non-existent user returns 404"""
    response = client.get("/plans/non-existent-user")
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}

def test_get_plan_success(tmp_path, monkeypatch):
    """Test that getting plans for an existing user returns the user's plans"""
    # Create temporary data directory structure
    data_dir = tmp_path / "data"
    user_dir = data_dir / "user123" / "training_plans"
    user_dir.mkdir(parents=True)
    
    # Create a sample plan file
    plan_data = {
        "id": "test-plan-123",
        "athlete_id": "12345",
        "name": "Test Plan",
        "description": "A test training plan"
    }
    
    plan_file = user_dir / "plan1.json"
    with open(plan_file, 'w') as f:
        import json
        json.dump(plan_data, f)
    
    # Mock the data directory path
    monkeypatch.chdir(tmp_path)
    
    response = client.get("/plans/user123")
    assert response.status_code == 200
    expected_response = {"user_id": "user123", "plans": [plan_data]}
    assert response.json() == expected_response
