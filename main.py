from datetime import date
from pawpal_system import Owner, Pet, Task, Scheduler


def main():
    # Create owner
    owner = Owner(owner_id=1, name="Apoorva")

    # Create pets
    pet1 = Pet(1, "Buddy", "Dog", "Golden Retriever", 3, 25.0)
    pet2 = Pet(2, "Mittens", "Cat", "Siamese", 2, 8.0)

    # Add pets to owner
    owner.add_pet(pet1)
    owner.add_pet(pet2)

    # Add tasks to pet1
    pet1.add_task(Task(
        task_id=1,
        title="Morning Walk",
        description="Take Buddy for a walk",
        scheduled_time="09:00",
        duration=30,
        frequency="daily",
        due_date=date.today(),
    ))

    pet1.add_task(Task(
        task_id=2,
        title="Feeding",
        description="Feed Buddy breakfast",
        scheduled_time="08:00",
        duration=10,
        frequency="daily",
        due_date=date.today(),
    ))

    # Add tasks to pet2
    pet2.add_task(Task(
        task_id=3,
        title="Playtime",
        description="Play with Mittens",
        scheduled_time="09:00",
        duration=20,
        frequency="daily",
        due_date=date.today(),
    ))

    pet2.add_task(Task(
        task_id=4,
        title="Grooming",
        description="Brush Mittens",
        scheduled_time="11:00",
        duration=15,
        frequency="weekly",
        due_date=date.today(),
    ))

    # Create scheduler
    scheduler = Scheduler(owner)

    # Print schedule
    print("\n===== Today's Schedule =====\n")
    print(scheduler.format_schedule_for_terminal())


if __name__ == "__main__":
    main()