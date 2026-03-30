from pawpal_system import Owner, Pet, CareTask, TaskManager, Scheduler


def main():
    # Create Owner
    owner = Owner(
        owner_id=1,
        name="Apoorva",
        available_time_per_day=120  # minutes
    )

    # Create Pets
    pet1 = Pet(1, "Buddy", "Dog", "Golden Retriever", 3, 25.0)
    pet2 = Pet(2, "Mittens", "Cat", "Siamese", 2, 8.0)

    # Add pets to owner
    owner.add_pet(pet1)
    owner.add_pet(pet2)

    # Create TaskManager
    task_manager = TaskManager()

    # Add tasks for pet1 (Dog)
    task_manager.add_task(CareTask(
        task_id=1,
        pet_id=1,
        title="Morning Walk",
        category="Exercise",
        duration=30,
        priority=3,
        frequency="Daily",
        is_required=True
    ))

    task_manager.add_task(CareTask(
        task_id=2,
        pet_id=1,
        title="Feeding",
        category="Food",
        duration=10,
        priority=5,
        frequency="Daily",
        is_required=True
    ))

    # Add tasks for pet2 (Cat)
    task_manager.add_task(CareTask(
        task_id=3,
        pet_id=2,
        title="Playtime",
        category="Enrichment",
        duration=20,
        priority=2,
        frequency="Daily"
    ))

    task_manager.add_task(CareTask(
        task_id=4,
        pet_id=2,
        title="Grooming",
        category="Care",
        duration=15,
        priority=1,
        frequency="Weekly"
    ))

    # Create Scheduler for pet1
    scheduler = Scheduler(owner, pet1, task_manager)

    # Generate plan
    plan = scheduler.generate_plan()

    # Print Schedule
    print("\n===== Today's Schedule =====\n")
    print(plan.generate_summary())


if __name__ == "__main__":
    main()