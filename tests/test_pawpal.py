from pawpal_system import Pet, CareTask, TaskManager


def test_task_completion():
    # Create a task
    task = CareTask(
        task_id=1,
        pet_id=1,
        title="Walk",
        category="Exercise",
        duration=30,
        priority=3,
        frequency="Daily"
    )

    # Initially should be incomplete
    assert task.completed is False

    # Mark complete
    task.mark_complete()

    # Verify status changed
    assert task.completed is True


def test_task_addition_to_pet():
    # Create pet
    pet = Pet(1, "Buddy", "Dog", "Golden Retriever", 3, 25.0)

    # Create TaskManager
    task_manager = TaskManager()

    # Initially no tasks for this pet
    assert len(task_manager.get_tasks_for_pet(pet.pet_id)) == 0

    # Add a task
    task = CareTask(
        task_id=1,
        pet_id=pet.pet_id,
        title="Feeding",
        category="Food",
        duration=10,
        priority=5,
        frequency="Daily"
    )

    task_manager.add_task(task)

    # Verify task count increased
    assert len(task_manager.get_tasks_for_pet(pet.pet_id)) == 1