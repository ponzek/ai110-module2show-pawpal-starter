"""
PawPal+ Test Suite

Tests core behaviors:
1. Task completion (mark_complete changes status)
2. Task addition (adding tasks increases pet's task count)
3. Task validation (is_valid catches bad data)
4. Sorting correctness (tasks returned in chronological order)
5. Recurrence logic (completing a daily task creates the next day's task)
6. Conflict detection (scheduler flags overlapping time slots)
7. Edge cases (empty schedules, pet with no tasks, etc.)
"""

from datetime import date, timedelta
from pawpal_system import Owner, Pet, Task, Scheduler


# --- 1. Task Completion ---

class TestTaskCompletion:
    """Verify that calling mark_complete() actually changes the task's status."""

    def test_task_starts_incomplete(self):
        task = Task(title="Morning walk", duration_minutes=30, priority="high")
        assert task.completed is False

    def test_mark_complete_changes_status(self):
        task = Task(title="Morning walk", duration_minutes=30, priority="high")
        task.mark_complete()
        assert task.completed is True

    def test_mark_complete_is_idempotent(self):
        task = Task(title="Feeding", duration_minutes=10)
        task.mark_complete()
        task.mark_complete()
        assert task.completed is True


# --- 2. Task Addition ---

class TestTaskAddition:
    """Verify that adding a task to a Pet increases that pet's task count."""

    def test_pet_starts_with_no_tasks(self):
        pet = Pet(name="Mochi", species="dog")
        assert len(pet.get_tasks()) == 0

    def test_adding_one_task_increases_count(self):
        pet = Pet(name="Mochi", species="dog")
        pet.add_task(Task(title="Walk", duration_minutes=30, priority="high"))
        assert len(pet.get_tasks()) == 1

    def test_adding_multiple_tasks(self):
        pet = Pet(name="Whiskers", species="cat")
        pet.add_task(Task(title="Feed", duration_minutes=10, priority="high"))
        pet.add_task(Task(title="Play", duration_minutes=15, priority="low"))
        pet.add_task(Task(title="Groom", duration_minutes=20, priority="medium"))
        assert len(pet.get_tasks()) == 3

    def test_remove_task_decreases_count(self):
        pet = Pet(name="Mochi", species="dog")
        pet.add_task(Task(title="Walk", duration_minutes=30))
        pet.add_task(Task(title="Feed", duration_minutes=10))
        pet.remove_task("Walk")
        assert len(pet.get_tasks()) == 1
        assert pet.get_tasks()[0].title == "Feed"


# --- 3. Task Validation ---

class TestTaskValidation:
    """Verify that is_valid() correctly validates task data."""

    def test_valid_task(self):
        task = Task(title="Walk", duration_minutes=30, priority="high")
        assert task.is_valid() is True

    def test_empty_title_is_invalid(self):
        task = Task(title="", duration_minutes=30, priority="high")
        assert task.is_valid() is False

    def test_zero_duration_is_invalid(self):
        task = Task(title="Walk", duration_minutes=0, priority="high")
        assert task.is_valid() is False

    def test_bad_priority_is_invalid(self):
        task = Task(title="Walk", duration_minutes=30, priority="urgent")
        assert task.is_valid() is False


# --- 4. Sorting Correctness ---

class TestSorting:
    """Verify tasks are returned in the correct order."""

    def test_sort_by_time_returns_chronological_order(self):
        owner = Owner(name="Test", available_minutes=120)
        pet = Pet(name="Rex", species="dog")
        owner.add_pet(pet)
        scheduler = Scheduler(owner)

        tasks = [
            Task(title="Lunch walk", duration_minutes=20, preferred_time="12:00"),
            Task(title="Morning feed", duration_minutes=10, preferred_time="07:00"),
            Task(title="Evening meds", duration_minutes=5, preferred_time="18:00"),
        ]

        sorted_tasks = scheduler.sort_by_time(tasks)
        assert sorted_tasks[0].title == "Morning feed"
        assert sorted_tasks[1].title == "Lunch walk"
        assert sorted_tasks[2].title == "Evening meds"

    def test_sort_by_time_puts_no_time_last(self):
        owner = Owner(name="Test", available_minutes=120)
        pet = Pet(name="Rex", species="dog")
        owner.add_pet(pet)
        scheduler = Scheduler(owner)

        tasks = [
            Task(title="No time task", duration_minutes=10),
            Task(title="Morning task", duration_minutes=10, preferred_time="08:00"),
        ]

        sorted_tasks = scheduler.sort_by_time(tasks)
        assert sorted_tasks[0].title == "Morning task"
        assert sorted_tasks[1].title == "No time task"

    def test_sort_by_priority_high_first(self):
        owner = Owner(name="Test", available_minutes=120)
        pet = Pet(name="Rex", species="dog")
        owner.add_pet(pet)
        scheduler = Scheduler(owner)

        tasks = [
            Task(title="Low task", duration_minutes=10, priority="low"),
            Task(title="High task", duration_minutes=10, priority="high"),
            Task(title="Medium task", duration_minutes=10, priority="medium"),
        ]

        sorted_tasks = scheduler.sort_by_priority(tasks)
        assert sorted_tasks[0].title == "High task"
        assert sorted_tasks[1].title == "Medium task"
        assert sorted_tasks[2].title == "Low task"


# --- 5. Recurrence Logic ---

class TestRecurrence:
    """Confirm that marking a daily task complete creates a new task for the next day."""

    def test_daily_task_creates_next_day(self):
        owner = Owner(name="Test", available_minutes=120)
        pet = Pet(name="Rex", species="dog")
        owner.add_pet(pet)

        today = date.today()
        task = Task(
            title="Morning walk",
            duration_minutes=30,
            priority="high",
            is_recurring=True,
            frequency="daily",
            due_date=today,
        )
        pet.add_task(task)
        task.mark_complete()

        scheduler = Scheduler(owner)
        next_task = scheduler.handle_recurring(task, pet)

        assert next_task is not None
        assert next_task.due_date == today + timedelta(days=1)
        assert next_task.completed is False
        assert len(pet.get_tasks()) == 2

    def test_weekly_task_creates_next_week(self):
        owner = Owner(name="Test", available_minutes=120)
        pet = Pet(name="Rex", species="dog")
        owner.add_pet(pet)

        today = date.today()
        task = Task(
            title="Grooming",
            duration_minutes=60,
            priority="medium",
            is_recurring=True,
            frequency="weekly",
            due_date=today,
        )
        pet.add_task(task)
        task.mark_complete()

        scheduler = Scheduler(owner)
        next_task = scheduler.handle_recurring(task, pet)

        assert next_task is not None
        assert next_task.due_date == today + timedelta(weeks=1)

    def test_non_recurring_task_returns_none(self):
        owner = Owner(name="Test", available_minutes=120)
        pet = Pet(name="Rex", species="dog")
        owner.add_pet(pet)

        task = Task(title="Vet visit", duration_minutes=30, is_recurring=False)
        pet.add_task(task)

        scheduler = Scheduler(owner)
        result = scheduler.handle_recurring(task, pet)
        assert result is None


# --- 6. Conflict Detection ---

class TestConflictDetection:
    """Verify that the Scheduler flags duplicate/overlapping time slots."""

    def test_overlapping_tasks_detected(self):
        owner = Owner(name="Test", available_minutes=120)
        pet = Pet(name="Rex", species="dog")
        owner.add_pet(pet)
        scheduler = Scheduler(owner)

        # Two tasks at the exact same time
        schedule = [
            {"task": "Walk", "start": "08:00", "end": "08:30", "duration": 30, "priority": "high", "pet": "Rex", "category": "walk"},
            {"task": "Vet", "start": "08:00", "end": "08:25", "duration": 25, "priority": "high", "pet": "Rex", "category": "meds"},
        ]

        conflicts = scheduler.detect_conflicts(schedule)
        assert len(conflicts) == 1
        assert "Walk" in conflicts[0]
        assert "Vet" in conflicts[0]

    def test_no_conflicts_when_tasks_dont_overlap(self):
        owner = Owner(name="Test", available_minutes=120)
        pet = Pet(name="Rex", species="dog")
        owner.add_pet(pet)
        scheduler = Scheduler(owner)

        schedule = [
            {"task": "Walk", "start": "08:00", "end": "08:30", "duration": 30, "priority": "high", "pet": "Rex", "category": "walk"},
            {"task": "Feed", "start": "09:00", "end": "09:10", "duration": 10, "priority": "high", "pet": "Rex", "category": "feeding"},
        ]

        conflicts = scheduler.detect_conflicts(schedule)
        assert len(conflicts) == 0

    def test_back_to_back_tasks_no_conflict(self):
        owner = Owner(name="Test", available_minutes=120)
        pet = Pet(name="Rex", species="dog")
        owner.add_pet(pet)
        scheduler = Scheduler(owner)

        # One ends at 08:30, next starts at 08:30 - should NOT be a conflict
        schedule = [
            {"task": "Walk", "start": "08:00", "end": "08:30", "duration": 30, "priority": "high", "pet": "Rex", "category": "walk"},
            {"task": "Feed", "start": "08:30", "end": "08:40", "duration": 10, "priority": "high", "pet": "Rex", "category": "feeding"},
        ]

        conflicts = scheduler.detect_conflicts(schedule)
        assert len(conflicts) == 0


# --- 7. Edge Cases ---

class TestEdgeCases:
    """Test unusual situations the system should handle gracefully."""

    def test_schedule_with_no_tasks(self):
        owner = Owner(name="Test", available_minutes=120)
        pet = Pet(name="Rex", species="dog")
        owner.add_pet(pet)

        scheduler = Scheduler(owner)
        schedule = scheduler.generate_schedule()
        assert schedule == []

    def test_schedule_with_no_pets(self):
        owner = Owner(name="Test", available_minutes=120)
        scheduler = Scheduler(owner)
        schedule = scheduler.generate_schedule()
        assert schedule == []

    def test_explain_plan_with_empty_schedule(self):
        owner = Owner(name="Test", available_minutes=120)
        scheduler = Scheduler(owner)
        explanation = scheduler.explain_plan([])
        assert "No tasks scheduled" in explanation

    def test_filter_incomplete_skips_completed(self):
        owner = Owner(name="Test", available_minutes=120)
        pet = Pet(name="Rex", species="dog")
        owner.add_pet(pet)
        scheduler = Scheduler(owner)

        tasks = [
            Task(title="Done task", duration_minutes=10, completed=True),
            Task(title="Open task", duration_minutes=10, completed=False),
        ]

        result = scheduler.filter_incomplete(tasks)
        assert len(result) == 1
        assert result[0].title == "Open task"

    def test_schedule_respects_time_budget(self):
        owner = Owner(name="Test", available_minutes=30)
        pet = Pet(name="Rex", species="dog")
        pet.add_task(Task(title="Walk", duration_minutes=20, priority="high"))
        pet.add_task(Task(title="Play", duration_minutes=20, priority="low"))
        owner.add_pet(pet)

        scheduler = Scheduler(owner)
        schedule = scheduler.generate_schedule()

        total_scheduled = sum(e["duration"] for e in schedule)
        assert total_scheduled <= 30

    def test_filter_by_pet_returns_correct_tasks(self):
        owner = Owner(name="Test", available_minutes=120)
        dog = Pet(name="Rex", species="dog")
        cat = Pet(name="Luna", species="cat")
        dog.add_task(Task(title="Walk", duration_minutes=30))
        cat.add_task(Task(title="Feed", duration_minutes=10))
        owner.add_pet(dog)
        owner.add_pet(cat)

        scheduler = Scheduler(owner)
        rex_tasks = scheduler.filter_by_pet("Rex")
        assert len(rex_tasks) == 1
        assert rex_tasks[0].title == "Walk"

    def test_filter_by_nonexistent_pet(self):
        owner = Owner(name="Test", available_minutes=120)
        owner.add_pet(Pet(name="Rex", species="dog"))

        scheduler = Scheduler(owner)
        result = scheduler.filter_by_pet("Ghost")
        assert result == []


# --- 8. Knapsack Optimizer ---

class TestKnapsackOptimizer:
    """Verify the knapsack algorithm picks the best combination of tasks."""

    def test_knapsack_picks_higher_value_over_greedy(self):
        """The greedy approach would pick the first high-priority task and run out
        of time, but knapsack should find a better combination."""
        owner = Owner(name="Test", available_minutes=30)
        pet = Pet(name="Rex", species="dog")

        # Greedy picks the 25-min high task first, leaving only 5 min (can't fit anything else)
        # Knapsack should pick the two medium tasks (15+15=30 min, value 2+2=4)
        # instead of the one high task (25 min, value 3)
        pet.add_task(Task(title="Big walk", duration_minutes=25, priority="high"))
        pet.add_task(Task(title="Feed AM", duration_minutes=15, priority="medium"))
        pet.add_task(Task(title="Feed PM", duration_minutes=15, priority="medium"))
        owner.add_pet(pet)

        scheduler = Scheduler(owner)
        result = scheduler.optimize_knapsack(pet.get_tasks(), 30)

        total_value = sum({"high": 3, "medium": 2, "low": 1}[t.priority] for t in result)
        total_duration = sum(t.duration_minutes for t in result)

        # Knapsack should get value 4 (two mediums) instead of 3 (one high)
        assert total_value == 4
        assert total_duration <= 30

    def test_knapsack_with_empty_tasks(self):
        owner = Owner(name="Test", available_minutes=60)
        pet = Pet(name="Rex", species="dog")
        owner.add_pet(pet)

        scheduler = Scheduler(owner)
        result = scheduler.optimize_knapsack([], 60)
        assert result == []

    def test_knapsack_respects_capacity(self):
        owner = Owner(name="Test", available_minutes=20)
        pet = Pet(name="Rex", species="dog")
        pet.add_task(Task(title="Long walk", duration_minutes=60, priority="high"))
        owner.add_pet(pet)

        scheduler = Scheduler(owner)
        result = scheduler.optimize_knapsack(pet.get_tasks(), 20)

        # Task doesn't fit, should return nothing
        assert len(result) == 0

    def test_optimized_schedule_returns_valid_entries(self):
        owner = Owner(name="Test", available_minutes=60)
        pet = Pet(name="Rex", species="dog")
        pet.add_task(Task(title="Walk", duration_minutes=20, priority="high"))
        pet.add_task(Task(title="Feed", duration_minutes=10, priority="high"))
        owner.add_pet(pet)

        scheduler = Scheduler(owner)
        schedule = scheduler.generate_optimized_schedule()

        # Should have both tasks
        assert len(schedule) == 2
        # Each entry should have the right keys
        for entry in schedule:
            assert "task" in entry
            assert "start" in entry
            assert "end" in entry
            assert "priority" in entry
