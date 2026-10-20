from datetime import date, time, timedelta

from pawpal_system import Owner, Pet, Scheduler, Task


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

	assert scheduler.filter_tasks(completed=False) == [pending_task, other_pet_task]
	assert scheduler.filter_tasks(pet_name="MOCHI") == [completed_task, pending_task]
	assert scheduler.filter_tasks(completed=True, pet_name="mochi") == [completed_task]
