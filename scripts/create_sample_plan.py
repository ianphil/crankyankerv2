from datetime import datetime, timedelta
from app.training_plan.plan import Plan, Phase, Block, Workout, save_training_plan

# Create a sample cycling workout
cycling_workout = Workout(
    name="Zone 2 Base Ride",
    description="60-minute steady endurance ride in aerobic zone",
    duration=60,
    intensity="moderate"
)

# Create a training block
base_block = Block(
    name="Aerobic Base Block",
    start_date=datetime.now(),
    end_date=datetime.now() + timedelta(weeks=4),
    workouts=[cycling_workout]
)

# Create a phase
base_phase = Phase(
    name="Base Building Phase",
    description="Building aerobic capacity and endurance foundation",
    start_date=datetime.now(),
    end_date=datetime.now() + timedelta(weeks=4),
    blocks=[base_block]
)

# Create the complete cycling training plan
cycling_plan = Plan(
    athlete_id="cyclist_001",
    target_date=datetime.now() + timedelta(weeks=12),
    name="Cycling Base Training Plan",
    description="4-week aerobic base building plan for recreational cyclists",
    phases=[base_phase]
)

# Save the plan for sample user
user_id = "sample_user_123"
saved_path = save_training_plan(cycling_plan, user_id)
print(f"Sample cycling plan saved to: {saved_path}")
print(f"Plan ID: {cycling_plan.id}")