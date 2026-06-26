"""
PawPal+ System — Backend Logic Layer

Classes: Owner, Pet, Task, Scheduler
Uses Python dataclasses for clean, maintainable data objects.
"""

from dataclasses import dataclass, field
from typing import Optional


# Priority ranking for sorting (higher number = higher priority)
PRIORITY_RANK = {"high": 3, "medium": 2, "low": 1}


@dataclass
class Task:
    """Represents a single pet care task (walk, feeding, meds, etc.)."""

    title: str
    duration_minutes: int
    priority: str = "medium"  # "low", "medium", "high"
    category: str = "general"  # e.g. "walk", "feeding", "meds", "grooming", "enrichment"
    is_recurring: bool = False
    preferred_time: Optional[str] = None  # e.g. "08:00"
    completed: bool = False

    def is_valid(self) -> bool:
        """Return True if the task has a non-empty title, positive duration, and valid priority."""
        return (
            bool(self.title and self.title.strip())
            and self.duration_minutes > 0
            and self.priority in PRIORITY_RANK
        )

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.completed = True

    def __lt__(self, other: "Task") -> bool:
        """Compare tasks so higher-priority tasks sort first; ties broken by shorter duration."""
        if PRIORITY_RANK.get(self.priority, 0) != PRIORITY_RANK.get(other.priority, 0):
            # Higher priority value should come first, so reverse the comparison
            return PRIORITY_RANK.get(self.priority, 0) > PRIORITY_RANK.get(other.priority, 0)
        # For same priority, shorter tasks come first
        return self.duration_minutes < other.duration_minutes


@dataclass
class Pet:
    """Stores pet details and a list of care tasks."""

    name: str
    species: str
    age: int = 0
    special_needs: list[str] = field(default_factory=list)
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a care task to this pet's task list."""
        self.tasks.append(task)

    def remove_task(self, title: str) -> None:
        """Remove the first task matching the given title."""
        self.tasks = [t for t in self.tasks if t.title != title]

    def get_tasks(self) -> list[Task]:
        """Return all tasks assigned to this pet."""
        return list(self.tasks)


@dataclass
class Owner:
    """Manages multiple pets and provides access to all their tasks."""

    name: str
    available_minutes: int = 120  # default daily time budget
    preferences: list[str] = field(default_factory=list)
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Register a pet under this owner."""
        self.pets.append(pet)

    def set_availability(self, minutes: int) -> None:
        """Update the owner's daily available time in minutes."""
        self.available_minutes = minutes

    def get_pets(self) -> list[Pet]:
        """Return all pets belonging to this owner."""
        return list(self.pets)

    def get_all_tasks(self) -> list[Task]:
        """Retrieve all tasks across every pet owned."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.get_tasks())
        return all_tasks


class Scheduler:
    """The 'Brain' that retrieves, organizes, and manages tasks across pets."""

    def __init__(self, owner: Owner) -> None:
        """Initialize the scheduler with an owner and their time budget."""
        self.owner = owner
        self.total_minutes = owner.available_minutes

    def generate_schedule(self) -> list[dict]:
        """Build a daily schedule from all pets' tasks, respecting time and priority constraints."""
        # Gather all tasks from all pets
        all_tasks = self.owner.get_all_tasks()

        # Sort by priority (high first), then filter by available time
        sorted_tasks = self.sort_by_priority(all_tasks)
        scheduled_tasks = self.filter_by_time(sorted_tasks, self.total_minutes)

        # Build the schedule with time slots starting at 08:00
        schedule = []
        current_hour = 8
        current_minute = 0

        for task in scheduled_tasks:
            # Use preferred time if set, otherwise use next available slot
            if task.preferred_time:
                parts = task.preferred_time.split(":")
                start_hour = int(parts[0])
                start_min = int(parts[1])
            else:
                start_hour = current_hour
                start_min = current_minute

            end_total_min = start_hour * 60 + start_min + task.duration_minutes
            end_hour = end_total_min // 60
            end_min = end_total_min % 60

            # Find which pet this task belongs to
            pet_name = "Unknown"
            for pet in self.owner.get_pets():
                if task in pet.get_tasks():
                    pet_name = pet.name
                    break

            schedule.append({
                "pet": pet_name,
                "task": task.title,
                "start": f"{start_hour:02d}:{start_min:02d}",
                "end": f"{end_hour:02d}:{end_min:02d}",
                "duration": task.duration_minutes,
                "priority": task.priority,
                "category": task.category,
            })

            # Advance the clock for next unscheduled task
            current_hour = end_hour
            current_minute = end_min

        return schedule

    def sort_by_priority(self, tasks: list[Task]) -> list[Task]:
        """Sort tasks by priority (high first), then by shorter duration."""
        return sorted(tasks)

    def detect_conflicts(self, schedule: list[dict]) -> list[str]:
        """Identify overlapping time slots in the schedule."""
        conflicts = []
        for i in range(len(schedule)):
            for j in range(i + 1, len(schedule)):
                a = schedule[i]
                b = schedule[j]
                # Convert times to minutes for easy comparison
                a_start = int(a["start"].split(":")[0]) * 60 + int(a["start"].split(":")[1])
                a_end = int(a["end"].split(":")[0]) * 60 + int(a["end"].split(":")[1])
                b_start = int(b["start"].split(":")[0]) * 60 + int(b["start"].split(":")[1])
                b_end = int(b["end"].split(":")[0]) * 60 + int(b["end"].split(":")[1])

                if a_start < b_end and b_start < a_end:
                    conflicts.append(
                        f"Conflict: '{a['task']}' ({a['start']}-{a['end']}) "
                        f"overlaps with '{b['task']}' ({b['start']}-{b['end']})"
                    )
        return conflicts

    def filter_by_time(self, tasks: list[Task], available: int) -> list[Task]:
        """Select tasks that fit within the available time budget, in priority order."""
        selected = []
        remaining = available
        for task in tasks:
            if task.duration_minutes <= remaining:
                selected.append(task)
                remaining -= task.duration_minutes
        return selected

    def explain_plan(self, schedule: list[dict]) -> str:
        """Generate a human-readable explanation of why each task was scheduled."""
        if not schedule:
            return "No tasks scheduled for today."

        lines = []
        total_duration = sum(entry["duration"] for entry in schedule)
        lines.append(f">> Today's Plan ({len(schedule)} tasks, {total_duration} min total):\n")

        for i, entry in enumerate(schedule, 1):
            reason = []
            if entry["priority"] == "high":
                reason.append("high priority — scheduled first")
            elif entry["priority"] == "medium":
                reason.append("medium priority")
            else:
                reason.append("low priority — fit into remaining time")

            lines.append(
                f"  {i}. {entry['start']} — {entry['task']} for {entry['pet']} "
                f"({entry['duration']} min) [{entry['priority']}]"
            )
            lines.append(f"     Reason: {', '.join(reason)}")

        remaining = self.total_minutes - total_duration
        lines.append(f"\n>> Time remaining: {remaining} min out of {self.total_minutes} min budget")

        return "\n".join(lines)
