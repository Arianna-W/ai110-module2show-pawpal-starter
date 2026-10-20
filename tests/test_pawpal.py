from datetime import date, time, timedelta

from pawpal_system import Owner, Pet, Scheduler, Task
from pawpal_formatting import format_priority, format_status, format_task_name


def test_formatting_helpers_add_task_type_priority_and_status_indicators():
	assert format_task_name("Morning walk") == "🚶 Morning walk"
	assert format_task_name("Medication") == "💊 Medication"
	assert format_task_name("Breakfast") == "🍽️ Breakfast"
	assert format_task_name("Uncategorized") == "🐾 Uncategorized"
	assert format_priority("High") == "🔴 High"
	assert format_priority("Medium") == "🟡 Medium"
	assert format_priority("Low") == "🟢 Low"
	assert format_status(True) == "✅ Completed"
	assert format_status(False) == "🟠 To do"


def test_scheduler_mark_task_completed_updates_task_status():
	owner = Owner(name="Jordan", address="123 Paw Street")
	pet = Pet(name="Mochi", age=3, pet_type="cat", breed="Tabby")
	task = Task.create_task(
		name="Medication",
		description="Give the evening dose",
		duration=5,
		priority=1,
	)
	owner.add_pet_information(pet)
	pet.add_task(task)
	scheduler = Scheduler(owner)

	scheduler.mark_task_completed(task)

	assert task.completed is True


def test_scheduler_completion_creates_next_daily_occurrence():
	owner = Owner(name="Jordan", address="123 Paw Street")
	pet = Pet(name="Mochi", age=3, pet_type="cat", breed="Tabby")
	task = Task.create_task(
		name="Medication",
		description="Give the morning dose",
		duration=5,
		priority=3,
		frequency="daily",
	)
	owner.add_pet_information(pet)
	pet.add_task(task)
	scheduler = Scheduler(owner)
	scheduler.daily_schedule = [task]
	today = date.today()

	scheduler.mark_task_completed(task)

	assert task.completed is True
	assert len(pet.tasks) == 2
	next_task = pet.tasks[1]
	assert next_task is not task
	assert next_task.due_date == today + timedelta(days=1)
	assert next_task.completed is False
	assert scheduler.daily_schedule == []
	assert scheduler.create_daily_schedule() == []


def test_scheduler_completion_creates_next_weekly_occurrence():
	owner = Owner(name="Jordan", address="123 Paw Street")
	pet = Pet(name="Mochi", age=3, pet_type="cat", breed="Tabby")
	task = Task.create_task(
		name="Grooming",
		description="Brush coat",
		duration=15,
		priority=2,
		frequency="weekly",
	)
	owner.add_pet_information(pet)
	pet.add_task(task)
	scheduler = Scheduler(owner)
	today = date.today()

	scheduler.mark_task_completed(task)

	assert task.completed is True
	assert len(pet.tasks) == 2
	assert pet.tasks[1].due_date == today + timedelta(days=7)


def test_pet_add_task_increases_task_count():
	pet = Pet(name="Biscuit", age=5, pet_type="dog", breed="Poodle")
	task = Task.create_task(
		name="Walk",
		description="Take a short walk",
		duration=15,
		priority=2,
	)
	initial_task_count = len(pet.tasks)

	pet.add_task(task)

	assert len(pet.tasks) == initial_task_count + 1


def test_owner_add_pet_and_collect_tasks_without_duplicates():
	owner = Owner(name="Jordan", address="123 Paw Street")
	pet = Pet(name="Mochi", age=3, pet_type="cat", breed="Tabby")
	task = Task.create_task(
		name="Breakfast", description="Serve breakfast", duration=10, priority=2,
	)
	pet.add_task(task)

	owner.add_pet_information(pet)
	owner.add_pet_information(pet)

	assert owner.pets == [pet]
	assert owner.get_all_tasks() == [task]


def test_owner_json_round_trip_preserves_pets_and_task_fields(tmp_path):
	owner = Owner(name="Jordan", address="123 Paw Street")
	mochi = Pet(name="Mochi", age=3, pet_type="cat", breed="Tabby")
	biscuit = Pet(name="Biscuit", age=5, pet_type="dog", breed="Poodle")
	completed_task = Task.create_task(
		name="Medication",
		description="Give the evening dose",
		duration=5,
		priority=3,
		scheduled_start=time(18, 15),
		frequency="weekly",
		completed=True,
		due_date=date(2026, 10, 18),
	)
	unscheduled_task = Task.create_task(
		name="Walk",
		description="Take a short walk",
		duration=20,
		priority=2,
	)
	mochi.add_task(completed_task)
	biscuit.add_task(unscheduled_task)
	owner.add_pet_information(mochi)
	owner.add_pet_information(biscuit)
	file_path = tmp_path / "data.json"

	owner.save_to_json(file_path)
	loaded_owner = Owner.load_from_json(file_path)

	assert loaded_owner == owner
	assert loaded_owner.pets[0].tasks[0].scheduled_start == time(18, 15)
	assert loaded_owner.pets[0].tasks[0].due_date == date(2026, 10, 18)
	assert loaded_owner.pets[1].tasks[0].scheduled_start is None
	assert loaded_owner.pets[1].tasks[0].due_date is None


def test_task_edit_and_delete():
	pet = Pet(name="Mochi", age=3, pet_type="cat", breed="Tabby")
	task = Task.create_task(
		name="Breakfast", description="Serve breakfast", duration=10, priority=2,
	)
	pet.add_task(task)

	task.edit_task("Brunch", "Serve a later meal", 15, 3)

	assert (task.name, task.description, task.duration, task.priority) == (
		"Brunch", "Serve a later meal", 15, 3
	)
	task.delete_task(pet)

	assert pet.tasks == []


def test_task_priority_level_labels():
	tasks = [
		Task.create_task("Low", "", 1, 1),
		Task.create_task("Medium", "", 1, 2),
		Task.create_task("High", "", 1, 3),
	]

	assert [task.priority_level for task in tasks] == ["Low", "Medium", "High"]


def test_scheduler_sort_by_time_orders_tasks_and_puts_unscheduled_last():
	owner = Owner(name="Jordan", address="123 Paw Street")
	pet = Pet(name="Mochi", age=3, pet_type="cat", breed="Tabby")
	late_task = Task.create_task(
		name="Dinner", description="Serve dinner", duration=10, priority=2,
		scheduled_start=time(18, 0),
	)
	unscheduled_task = Task.create_task(
		name="Brush", description="Brush coat", duration=5, priority=1,
	)
	early_task = Task.create_task(
		name="Breakfast", description="Serve breakfast", duration=10, priority=2,
		scheduled_start=time(7, 30),
	)
	for task in (late_task, unscheduled_task, early_task):
		pet.add_task(task)
	owner.add_pet_information(pet)

	scheduler = Scheduler(owner)

	assert scheduler.sort_by_time() == [early_task, late_task, unscheduled_task]


def test_scheduler_sort_by_priority_then_time():
	owner = Owner(name="Jordan", address="123 Paw Street")
	pet = Pet(name="Mochi", age=3, pet_type="cat", breed="Tabby")
	low_priority = Task.create_task(
		name="Breakfast", description="Serve breakfast", duration=10,
		priority=1, scheduled_start=time(7, 0),
	)
	medium_priority = Task.create_task(
		name="Walk", description="Take a walk", duration=20,
		priority=2, scheduled_start=time(8, 0),
	)
	high_priority_late = Task.create_task(
		name="Medication", description="Give medicine", duration=5,
		priority=3, scheduled_start=time(9, 0),
	)
	high_priority_early = Task.create_task(
		name="Water", description="Refresh water", duration=2,
		priority=3, scheduled_start=time(8, 30),
	)
	for task in (low_priority, medium_priority, high_priority_late, high_priority_early):
		pet.add_task(task)
	owner.add_pet_information(pet)
	scheduler = Scheduler(owner)

	assert scheduler.sort_by_time() == [
		high_priority_early,
		high_priority_late,
		medium_priority,
		low_priority,
	]


def test_daily_schedule_excludes_completed_and_future_tasks():
	owner = Owner(name="Jordan", address="123 Paw Street")
	pet = Pet(name="Mochi", age=3, pet_type="cat", breed="Tabby")
	today = date.today()
	due_today = Task.create_task(
		name="Breakfast", description="Serve breakfast", duration=10,
		priority=2, scheduled_start=time(8, 0), due_date=today,
	)
	no_due_date = Task.create_task(
		name="Walk", description="Take a walk", duration=20, priority=2,
		scheduled_start=time(9, 0),
	)
	completed = Task.create_task(
		name="Medication", description="Give medicine", duration=5,
		priority=3, completed=True,
	)
	future = Task.create_task(
		name="Grooming", description="Brush coat", duration=15, priority=1,
		due_date=today + timedelta(days=1),
	)
	for task in (future, completed, no_due_date, due_today):
		pet.add_task(task)
	owner.add_pet_information(pet)
	scheduler = Scheduler(owner)

	assert scheduler.create_daily_schedule() == [due_today, no_due_date]


def test_scheduler_detects_overlapping_tasks_with_warning():
	owner = Owner(name="Jordan", address="123 Paw Street")
	pet = Pet(name="Mochi", age=3, pet_type="cat", breed="Tabby")
	breakfast = Task.create_task(
		name="Breakfast",
		description="Serve breakfast",
		duration=20,
		priority=2,
		scheduled_start=time(8, 0),
	)
	medication = Task.create_task(
		name="Medication",
		description="Give medicine",
		duration=10,
		priority=3,
		scheduled_start=time(8, 15),
	)
	pet.add_task(breakfast)
	pet.add_task(medication)
	owner.add_pet_information(pet)
	scheduler = Scheduler(owner)

	schedule = scheduler.create_daily_schedule()

	assert len(schedule) == 2
	assert scheduler.detect_conflicts(schedule) == [
		"Warning: 'Breakfast' overlaps with 'Medication'."
	]
	assert scheduler.conflict_warnings == scheduler.detect_conflicts(schedule)


def test_scheduler_detects_tasks_with_duplicate_start_times():
	owner = Owner(name="Jordan", address="123 Paw Street")
	pet = Pet(name="Mochi", age=3, pet_type="cat", breed="Tabby")
	breakfast = Task.create_task(
		name="Breakfast", description="Serve breakfast", duration=10,
		priority=2, scheduled_start=time(8, 0),
	)
	medication = Task.create_task(
		name="Medication", description="Give medicine", duration=5,
		priority=3, scheduled_start=time(8, 0),
	)
	pet.add_task(breakfast)
	pet.add_task(medication)
	owner.add_pet_information(pet)
	scheduler = Scheduler(owner)

	schedule = scheduler.create_daily_schedule()

	assert schedule == [medication, breakfast]
	assert scheduler.conflict_warnings == [
		"Warning: 'Medication' overlaps with 'Breakfast'."
	]


def test_scheduler_filter_tasks_by_completion_and_pet_name():
	owner = Owner(name="Jordan", address="123 Paw Street")
	mochi = Pet(name="Mochi", age=3, pet_type="cat", breed="Tabby")
	biscuit = Pet(name="Biscuit", age=5, pet_type="dog", breed="Poodle")
	completed_task = Task.create_task(
		name="Medication", description="Give medicine", duration=5,
		priority=3, completed=True,
	)
	pending_task = Task.create_task(
		name="Breakfast", description="Serve breakfast", duration=10,
		priority=2,
	)
	other_pet_task = Task.create_task(
		name="Walk", description="Take a walk", duration=20, priority=2,
	)
	mochi.add_task(completed_task)
	mochi.add_task(pending_task)
	biscuit.add_task(other_pet_task)
	owner.add_pet_information(mochi)
	owner.add_pet_information(biscuit)
	scheduler = Scheduler(owner)

	assert scheduler.filter_tasks() == [completed_task, pending_task, other_pet_task]
	assert scheduler.filter_tasks(completed=False) == [pending_task, other_pet_task]
	assert scheduler.filter_tasks(pet_name="MOCHI") == [completed_task, pending_task]
	assert scheduler.filter_tasks(completed=True, pet_name="mochi") == [completed_task]
