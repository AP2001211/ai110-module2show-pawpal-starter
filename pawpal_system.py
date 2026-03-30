from dataclasses import dataclass, field, asdict
from datetime import date
from typing import List, Optional


# ---------------------------------------------------------------------------
# Data-only classes
# ---------------------------------------------------------------------------

@dataclass
class Pet:
    pet_id: int
    name: str
    species: str
    breed: str
    age: int
    weight: float
    special_needs: List[str] = field(default_factory=list)
    energy_level: str = ""

    def update_profile(self, **updates) -> None:
        for key, value in updates.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def add_special_need(self, need: str) -> None:
        if need and need not in self.special_needs:
            self.special_needs.append(need)

    def remove_special_need(self, need: str) -> None:
        if need in self.special_needs:
            self.special_needs.remove(need)

    def view_profile(self) -> dict:
        return asdict(self)


@dataclass
class CareTask:
    task_id: int
    pet_id: int
    title: str
    category: str
    duration: int                    # minutes
    priority: int                    # higher number = higher priority
    frequency: str
    preferred_time: str = ""
    is_required: bool = False
    notes: str = ""
    completed: bool = False

    def update_task(self, **updates) -> None:
        for key, value in updates.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def mark_complete(self) -> None:
        self.completed = True

    def mark_incomplete(self) -> None:
        self.completed = False

    def get_task_details(self) -> dict:
        return asdict(self)


@dataclass
class Recommendation:
    selected_tasks: List[CareTask] = field(default_factory=list)
    skipped_tasks: List[CareTask] = field(default_factory=list)
    reasons: List[str] = field(default_factory=list)

    def add_reason(self, reason: str) -> None:
        if reason:
            self.reasons.append(reason)

    def generate_explanation(self) -> str:
        if not self.reasons:
            return "No explanation available."
        return "\n".join(self.reasons)

    def show_skipped_reasons(self) -> List[str]:
        return self.reasons


@dataclass
class DailyPlan:
    date: date
    tasks_for_today: List[CareTask] = field(default_factory=list)
    available_time: int = 0          # minutes
    explanation: str = ""
    recommendation: Optional[Recommendation] = None

    @property
    def total_duration(self) -> int:
        return sum(task.duration for task in self.tasks_for_today)

    @property
    def unused_time(self) -> int:
        return max(0, self.available_time - self.total_duration)

    def add_task(self, task: CareTask) -> bool:
        if self.total_duration + task.duration <= self.available_time:
            self.tasks_for_today.append(task)
            return True
        return False

    def remove_task(self, task: CareTask) -> None:
        if task in self.tasks_for_today:
            self.tasks_for_today.remove(task)

    def calculate_total_duration(self) -> int:
        return self.total_duration

    def generate_summary(self) -> str:
        if not self.tasks_for_today:
            return f"Plan for {self.date}: No tasks scheduled."

        lines = [f"Plan for {self.date}:"]
        for task in self.tasks_for_today:
            lines.append(
                f"- {task.title} ({task.category}, {task.duration} min, priority {task.priority})"
            )
        lines.append(f"Total duration: {self.total_duration} minutes")
        lines.append(f"Unused time: {self.unused_time} minutes")

        if self.explanation:
            lines.append("Explanation:")
            lines.append(self.explanation)

        return "\n".join(lines)

    def clear_plan(self) -> None:
        self.tasks_for_today.clear()
        self.explanation = ""
        self.recommendation = None


# ---------------------------------------------------------------------------
# Behaviour-heavy classes
# ---------------------------------------------------------------------------

class Owner:
    def __init__(
        self,
        owner_id: int,
        name: str,
        available_time_per_day: int,
        preferred_time_blocks: str = "",
        notes: str = "",
    ):
        self.owner_id = owner_id
        self.name = name
        self.available_time_per_day = available_time_per_day   # source of truth
        self.preferred_time_blocks = preferred_time_blocks
        self.notes = notes
        self.pets: List[Pet] = []

    def update_info(self, **updates) -> None:
        for key, value in updates.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def set_availability(self, minutes: int) -> None:
        if minutes < 0:
            raise ValueError("Available time cannot be negative.")
        self.available_time_per_day = minutes

    def set_preferences(self, preferred_time_blocks: str) -> None:
        self.preferred_time_blocks = preferred_time_blocks

    def add_pet(self, pet: Pet) -> None:
        if pet not in self.pets:
            self.pets.append(pet)

    def get_all_pet_ids(self) -> List[int]:
        """Return the pet_ids for every pet this owner has."""
        return [pet.pet_id for pet in self.pets]

    def view_summary(self) -> dict:
        return {
            "owner_id": self.owner_id,
            "name": self.name,
            "available_time_per_day": self.available_time_per_day,
            "preferred_time_blocks": self.preferred_time_blocks,
            "notes": self.notes,
            "pets": [pet.view_profile() for pet in self.pets],
        }


class Constraint:
    def __init__(
        self,
        preferred_hours: str = "",
        must_do_tasks: Optional[List[int]] = None,
        skipped_task_rules: str = "",
    ):
        self.preferred_hours = preferred_hours
        self.must_do_task_ids: List[int] = must_do_tasks or []
        self.skipped_task_rules = skipped_task_rules

    def is_must_do(self, task: CareTask) -> bool:
        return task.is_required or task.task_id in self.must_do_task_ids

    def validate_task(self, task: CareTask, used_time: int, time_limit: int) -> bool:
        if task.duration < 0:
            return False
        return used_time + task.duration <= time_limit

    def allows(self, task: CareTask, used_time: int, time_limit: int) -> bool:
        return self.validate_task(task, used_time, time_limit)

    def update_constraint(
        self,
        preferred_hours: Optional[str] = None,
        must_do_tasks: Optional[List[int]] = None,
        skipped_task_rules: Optional[str] = None,
    ) -> None:
        if preferred_hours is not None:
            self.preferred_hours = preferred_hours
        if must_do_tasks is not None:
            self.must_do_task_ids = must_do_tasks
        if skipped_task_rules is not None:
            self.skipped_task_rules = skipped_task_rules


class TaskManager:
    def __init__(self):
        self.tasks: List[CareTask] = []

    def add_task(self, task: CareTask) -> None:
        if self.get_task_by_id(task.task_id) is not None:
            raise ValueError(f"Task with id {task.task_id} already exists.")
        self.tasks.append(task)

    def edit_task(self, task_id: int, **updates) -> bool:
        task = self.get_task_by_id(task_id)
        if task is None:
            return False
        task.update_task(**updates)
        return True

    def delete_task(self, task_id: int) -> bool:
        task = self.get_task_by_id(task_id)
        if task is None:
            return False
        self.tasks.remove(task)
        return True

    def get_all_tasks(self) -> List[CareTask]:
        return list(self.tasks)

    def get_task_by_id(self, task_id: int) -> Optional[CareTask]:
        for task in self.tasks:
            if task.task_id == task_id:
                return task
        return None

    def get_tasks_for_pet(self, pet_id: int) -> List[CareTask]:
        return [task for task in self.tasks if task.pet_id == pet_id]


class Scheduler:
    def __init__(
        self,
        owner: Owner,
        pet: Pet,
        task_manager: TaskManager,
        scheduling_rules: str = "",
        constraint: Optional[Constraint] = None,
    ):
        self.owner = owner
        self.pet = pet
        self.task_manager = task_manager
        self.scheduling_rules = scheduling_rules
        self.constraint = constraint or Constraint()
        self.daily_plan: Optional[DailyPlan] = None

    def sort_tasks_by_priority(self, tasks: Optional[List[CareTask]] = None) -> List[CareTask]:
        if tasks is None:
            tasks = self.task_manager.get_tasks_for_pet(self.pet.pet_id)

        return sorted(
            tasks,
            key=lambda task: (
                not self.constraint.is_must_do(task),  # must-do / required first
                -task.priority,                        # higher priority first
                task.duration,                         # shorter task first as tie-breaker
                task.title.lower(),
            ),
        )

    def filter_tasks_by_constraints(self, tasks: Optional[List[CareTask]] = None) -> List[CareTask]:
        if tasks is None:
            tasks = self.task_manager.get_tasks_for_pet(self.pet.pet_id)

        filtered = []
        used_time = 0
        time_limit = self.owner.available_time_per_day

        for task in self.sort_tasks_by_priority(tasks):
            if self.constraint.allows(task, used_time, time_limit):
                filtered.append(task)
                used_time += task.duration

        return filtered

    def check_time_limit(self, duration: int) -> bool:
        return duration <= self.owner.available_time_per_day

    def generate_plan(self) -> DailyPlan:
        pet_tasks = self.task_manager.get_tasks_for_pet(self.pet.pet_id)
        sorted_tasks = self.sort_tasks_by_priority(pet_tasks)

        plan = DailyPlan(
            date=date.today(),
            available_time=self.owner.available_time_per_day,
            recommendation=Recommendation(),
        )

        used_time = 0
        selected_tasks: List[CareTask] = []
        skipped_tasks: List[CareTask] = []
        reasons: List[str] = []

        for task in sorted_tasks:
            is_must_do = self.constraint.is_must_do(task)

            if self.constraint.allows(task, used_time, self.owner.available_time_per_day):
                plan.tasks_for_today.append(task)
                selected_tasks.append(task)
                used_time += task.duration
                reasons.append(
                    f"Selected '{task.title}' because it fit the time limit and had priority {task.priority}."
                )
            else:
                skipped_tasks.append(task)
                if is_must_do:
                    reasons.append(
                        f"Could not schedule required task '{task.title}' because it exceeded the available time."
                    )
                else:
                    reasons.append(
                        f"Skipped '{task.title}' because there was not enough time remaining."
                    )

        plan.recommendation.selected_tasks = selected_tasks
        plan.recommendation.skipped_tasks = skipped_tasks
        plan.recommendation.reasons = reasons
        plan.explanation = plan.recommendation.generate_explanation()

        self.daily_plan = plan
        return plan

    def get_all_owner_tasks(self) -> List[CareTask]:
        """Retrieve every CareTask belonging to any pet owned by this owner."""
        return [
            task
            for pet in self.owner.pets
            for task in self.task_manager.get_tasks_for_pet(pet.pet_id)
        ]

    def explain_plan(self) -> str:
        if self.daily_plan is None:
            return "No plan has been generated yet."
        return self.daily_plan.explanation