"""
PawPal+ System — Backend Logic Layer
Classes: Owner, Pet, Task, Scheduler
Uses Python dataclasses for clean, maintainable data objects.
"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Task:
    """Represents a single pet care task (walk, feeding, meds, etc.)."""

    title: str
    duration_minutes: int
    priority: str = "medium"  # "low", "medium", "high"
    category: str = "general"  # e.g. "walk", "feeding", "meds", "grooming", "enrichment"
    is_recurring: bool = False
    preferred_time: Optional[str] = None  # e.g. "08:00"

    def is_valid(self) -> bool:
        """Check whether the task has valid data."""
        pass

    def __lt__(self, other: "Task") -> bool:
        """Allow sorting tasks by priority (high > medium > low)."""
        pass


@dataclass
class Pet:
    """Represents a pet with its care tasks."""

    name: str
    species: str
    age: int = 0
    special_needs: list[str] = field(default_factory=list)
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a care task for this pet."""
        pass

    def remove_task(self, title: str) -> None:
        """Remove a task by title."""
        pass

    def get_tasks(self) -> list[Task]:
        """Return all tasks for this pet."""
        pass


@dataclass
class Owner:
    """Represents the pet owner."""

    name: str
    available_minutes: int = 120  # default daily time budget
    preferences: list[str] = field(default_factory=list)
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Register a pet under this owner."""
        pass

    def set_availability(self, minutes: int) -> None:
        """Update the owner's daily available time."""
        pass

    def get_pets(self) -> list[Pet]:
        """Return all pets belonging to this owner."""
        pass


class Scheduler:
    """Generates and manages daily care schedules."""

    def __init__(self, owner: Owner) -> None:
        self.owner = owner
        self.total_minutes = owner.available_minutes

    def generate_schedule(self) -> list[dict]:
        """Build a daily schedule from all pets' tasks, respecting constraints."""
        pass

    def sort_by_priority(self, tasks: list[Task]) -> list[Task]:
        """Sort tasks by priority (high first), then by duration."""
        pass

    def detect_conflicts(self, schedule: list[dict]) -> list[str]:
        """Identify overlapping or conflicting time slots."""
        pass

    def filter_by_time(self, tasks: list[Task], available: int) -> list[Task]:
        """Filter tasks that fit within the available time budget."""
        pass

    def explain_plan(self, schedule: list[dict]) -> str:
        """Generate a human-readable explanation of the schedule."""
        pass
