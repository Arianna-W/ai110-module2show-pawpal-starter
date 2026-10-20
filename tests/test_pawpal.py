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
