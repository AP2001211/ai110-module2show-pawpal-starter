from dataclasses import dataclass, field, asdict
from datetime import date, timedelta
from typing import List, Optional


@dataclass
class Task:
    """Represents a single pet care task."""

    task_id: int
    title: str
    description: str
    scheduled_time: str           # format: "HH:MM"
    duration: int                 # minutes
    frequency: str                # one-time, daily, weekly
    due_date: date
    completed: bool = False

    def mark_complete(self) -> None:
        """Mark the task as complete."""
        self.completed = True

    def mark_incomplete(self) -> None:
        """Mark the task as incomplete."""
        self.completed = False

    def get_next_recurring_task(self, new_task_id: int) -> Optional["Task"]:
        """Create the next recurring task if this task repeats."""
        if self.frequency.lower() == "daily":
            next_date = self.due_date + timedelta(days=1)
        elif self.frequency.lower() == "weekly":
            next_date = self.due_date + timedelta(weeks=1)
        else:
            return None

        return Task(
            task_id=new_task_id,
            title=self.title,
            description=self.description,
            scheduled_time=self.scheduled_time,
            duration=self.duration,
            frequency=self.frequency,
            due_date=next_date,
            completed=False,
        )

    def to_dict(self) -> dict:
        """Return task details as a dictionary."""
        return asdict(self)


@dataclass
class Pet:
    """Stores pet details and that pet's tasks."""

    pet_id: int
    name: str
    species: str
    breed: str
    age: int
    weight: float
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to this pet."""
        self.tasks.append(task)

    def remove_task(self, task_id: int) -> bool:
        """Remove a task from this pet by task id."""
        task = self.get_task_by_id(task_id)
        if task is None:
            return False
        self.tasks.remove(task)
        return True

    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        """Get a task by its id."""
        for task in self.tasks:
            if task.task_id == task_id:
                return task
        return None

    def get_tasks_by_status(self, completed: bool) -> List[Task]:
        """Return tasks filtered by completion status."""
        return [task for task in self.tasks if task.completed == completed]

    def view_profile(self) -> dict:
        """Return pet details as a dictionary."""
        return {
            "pet_id": self.pet_id,
            "name": self.name,
            "species": self.species,
            "breed": self.breed,
            "age": self.age,
            "weight": self.weight,
            "task_count": len(self.tasks),
        }


class Owner:
    """Manages multiple pets and provides access to their tasks."""

    def __init__(self, owner_id: int, name: str):
        self.owner_id = owner_id
        self.name = name
        self.pets: List[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner."""
        self.pets.append(pet)

    def remove_pet(self, pet_id: int) -> bool:
        """Remove a pet by id."""
        pet = self.get_pet_by_id(pet_id)
        if pet is None:
            return False
        self.pets.remove(pet)
        return True

    def get_pet_by_id(self, pet_id: int) -> Optional[Pet]:
        """Get a pet by id."""
        for pet in self.pets:
            if pet.pet_id == pet_id:
                return pet
        return None

    def get_pet_by_name(self, pet_name: str) -> Optional[Pet]:
        """Get a pet by name."""
        for pet in self.pets:
            if pet.name.lower() == pet_name.lower():
                return pet
        return None

    def get_all_tasks(self) -> List[Task]:
        """Return all tasks across all pets."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.tasks)
        return all_tasks

    def get_all_tasks_with_pet_names(self) -> List[tuple[str, Task]]:
        """Return all tasks paired with pet names."""
        result = []
        for pet in self.pets:
            for task in pet.tasks:
                result.append((pet.name, task))
        return result

    def view_summary(self) -> dict:
        """Return owner summary."""
        return {
            "owner_id": self.owner_id,
            "name": self.name,
            "pet_count": len(self.pets),
            "pets": [pet.view_profile() for pet in self.pets],
        }


class Scheduler:
    """Retrieves, sorts, filters, and manages tasks across pets."""

    def __init__(self, owner: Owner):
        self.owner = owner
        self.next_task_id = self._calculate_next_task_id()

    def _calculate_next_task_id(self) -> int:
        """Calculate the next available task id."""
        all_tasks = self.owner.get_all_tasks()
        if not all_tasks:
            return 1
        return max(task.task_id for task in all_tasks) + 1

    def get_todays_tasks(self) -> List[tuple[str, Task]]:
        """Get all tasks due today across all pets."""
        today = date.today()
        return [
            (pet_name, task)
            for pet_name, task in self.owner.get_all_tasks_with_pet_names()
            if task.due_date == today
        ]

    def sort_by_time(self, tasks_with_pets: List[tuple[str, Task]]) -> List[tuple[str, Task]]:
        """Sort tasks by scheduled time."""
        return sorted(tasks_with_pets, key=lambda item: item[1].scheduled_time)

    def filter_by_status(
        self, tasks_with_pets: List[tuple[str, Task]], completed: bool
    ) -> List[tuple[str, Task]]:
        """Filter tasks by completion status."""
        return [item for item in tasks_with_pets if item[1].completed == completed]

    def filter_by_pet_name(
        self, tasks_with_pets: List[tuple[str, Task]], pet_name: str
    ) -> List[tuple[str, Task]]:
        """Filter tasks by pet name."""
        return [item for item in tasks_with_pets if item[0].lower() == pet_name.lower()]

    def detect_conflicts(self, tasks_with_pets: List[tuple[str, Task]]) -> List[str]:
        """Return warnings for tasks scheduled at the same exact time."""
        conflicts = []
        seen_times = {}

        for pet_name, task in tasks_with_pets:
            time_key = task.scheduled_time
            if time_key in seen_times:
                other_pet, other_task = seen_times[time_key]
                conflicts.append(
                    f"Conflict: '{other_task.title}' for {other_pet} and "
                    f"'{task.title}' for {pet_name} are both scheduled at {time_key}."
                )
            else:
                seen_times[time_key] = (pet_name, task)

        return conflicts

    def mark_task_complete(self, pet_name: str, task_id: int) -> bool:
        """Mark a task complete and create the next recurring task if needed."""
        pet = self.owner.get_pet_by_name(pet_name)
        if pet is None:
            return False

        task = pet.get_task_by_id(task_id)
        if task is None:
            return False

        task.mark_complete()

        next_task = task.get_next_recurring_task(self.next_task_id)
        if next_task is not None:
            pet.add_task(next_task)
            self.next_task_id += 1

        return True

    def generate_schedule(self) -> List[tuple[str, Task]]:
        """Return today's tasks sorted by time."""
        todays_tasks = self.get_todays_tasks()
        return self.sort_by_time(todays_tasks)

    def format_schedule_for_terminal(self) -> str:
        """Return a readable terminal schedule."""
        schedule = self.generate_schedule()
        if not schedule:
            return "Today's Schedule:\nNo tasks scheduled for today."

        lines = ["Today's Schedule:"]
        for pet_name, task in schedule:
            status = "Done" if task.completed else "Pending"
            lines.append(
                f"- {task.scheduled_time} | {pet_name} | {task.title} "
                f"({task.duration} min, {task.frequency}, {status})"
            )

        conflicts = self.detect_conflicts(schedule)
        if conflicts:
            lines.append("\nWarnings:")
            lines.extend(f"- {warning}" for warning in conflicts)

        return "\n".join(lines)