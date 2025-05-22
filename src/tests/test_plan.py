import pytest
from datetime import datetime, timedelta
from app.training_plan.plan import Plan, Phase, Block, Workout

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
