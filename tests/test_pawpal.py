"""
PawPal+ Test Suite

Tests core behaviors: task completion, task addition, scheduling logic.
"""

from pawpal_system import Owner, Pet, Task, Scheduler


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
        task.mark_complete()  # calling twice should still be True
        assert task.completed is True


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


class TestScheduler:
    """Verify basic scheduling behavior."""

    def test_schedule_respects_time_budget(self):
        owner = Owner(name="Test", available_minutes=30)
        pet = Pet(name="Rex", species="dog")
        pet.add_task(Task(title="Walk", duration_minutes=20, priority="high"))
        pet.add_task(Task(title="Play", duration_minutes=20, priority="low"))
        owner.add_pet(pet)

        scheduler = Scheduler(owner)
        schedule = scheduler.generate_schedule()

        total_scheduled = sum(e["duration"] for e in schedule)
        assert total_scheduled <= 30  # should not exceed budget

    def test_high_priority_scheduled_first(self):
        owner = Owner(name="Test", available_minutes=60)
        pet = Pet(name="Rex", species="dog")
        pet.add_task(Task(title="Play", duration_minutes=15, priority="low"))
        pet.add_task(Task(title="Meds", duration_minutes=5, priority="high"))
        owner.add_pet(pet)

        scheduler = Scheduler(owner)
        schedule = scheduler.generate_schedule()

        assert schedule[0]["task"] == "Meds"
        assert schedule[0]["priority"] == "high"
