from datetime import date, timedelta
from pawpal_system import Pet, Task, Owner, Scheduler


def test_task_completion():
    task = Task(
        task_id=1,
        title="Walk",
        description="Morning walk",
        scheduled_time="09:00",
        duration=30,
        frequency="daily",
        due_date=date.today(),
    )

    assert task.completed is False
    task.mark_complete()
    assert task.completed is True


def test_task_addition_to_pet():
    pet = Pet(1, "Buddy", "Dog", "Golden Retriever", 3, 25.0)
    assert len(pet.tasks) == 0

    task = Task(
        task_id=1,
        title="Feeding",
        description="Feed dog",
        scheduled_time="08:00",
        duration=10,
        frequency="daily",
        due_date=date.today(),
    )

    pet.add_task(task)
    assert len(pet.tasks) == 1


def test_sorting_correctness():
    owner = Owner(1, "Apoorva")
    pet = Pet(1, "Buddy", "Dog", "Golden Retriever", 3, 25.0)
    owner.add_pet(pet)

    pet.add_task(Task(
        task_id=1,
        title="Walk",
        description="Morning walk",
        scheduled_time="10:00",
        duration=30,
        frequency="daily",
        due_date=date.today(),
    ))
    pet.add_task(Task(
        task_id=2,
        title="Feeding",
        description="Breakfast",
        scheduled_time="08:00",
        duration=10,
        frequency="daily",
        due_date=date.today(),
    ))
    pet.add_task(Task(
        task_id=3,
        title="Medication",
        description="Give medicine",
        scheduled_time="09:00",
        duration=5,
        frequency="daily",
        due_date=date.today(),
    ))

    scheduler = Scheduler(owner)
    schedule = scheduler.generate_schedule()

    assert [task.title for _, task in schedule] == ["Feeding", "Medication", "Walk"]


def test_recurrence_logic_for_daily_task():
    owner = Owner(1, "Apoorva")
    pet = Pet(1, "Buddy", "Dog", "Golden Retriever", 3, 25.0)
    owner.add_pet(pet)

    pet.add_task(Task(
        task_id=1,
        title="Feeding",
        description="Daily feeding",
        scheduled_time="08:00",
        duration=10,
        frequency="daily",
        due_date=date.today(),
    ))

    scheduler = Scheduler(owner)
    success = scheduler.mark_task_complete("Buddy", 1)

    assert success is True
    assert pet.tasks[0].completed is True
    assert len(pet.tasks) == 2
    assert pet.tasks[1].due_date == date.today() + timedelta(days=1)
    assert pet.tasks[1].completed is False


def test_conflict_detection():
    owner = Owner(1, "Apoorva")
    pet1 = Pet(1, "Buddy", "Dog", "Golden Retriever", 3, 25.0)
    pet2 = Pet(2, "Mittens", "Cat", "Siamese", 2, 8.0)
    owner.add_pet(pet1)
    owner.add_pet(pet2)

    pet1.add_task(Task(
        task_id=1,
        title="Walk",
        description="Morning walk",
        scheduled_time="09:00",
        duration=30,
        frequency="daily",
        due_date=date.today(),
    ))
    pet2.add_task(Task(
        task_id=2,
        title="Feeding",
        description="Breakfast",
        scheduled_time="09:00",
        duration=10,
        frequency="daily",
        due_date=date.today(),
    ))

    scheduler = Scheduler(owner)
    schedule = scheduler.generate_schedule()
    conflicts = scheduler.detect_conflicts(schedule)

    assert len(conflicts) == 1
    assert "09:00" in conflicts[0]