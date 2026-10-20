from datetime import time

from pawpal_system import Owner, Pet, Scheduler, Task


def main() -> None:
	owner = Owner(name="Jordan", address="123 Paw Street")
	mochi = Pet(name="Mochi", age=3, pet_type="cat", breed="Tabby")
	biscuit = Pet(name="Biscuit", age=5, pet_type="dog", breed="Poodle")
	owner.add_pet_information(mochi)
	owner.add_pet_information(biscuit)

	mochi.add_task(
		Task.create_task(
			name="Breakfast",
			description="Serve Mochi's morning meal",
			duration=10,
			priority=2,
			scheduled_start=time(7, 30),
			frequency="daily",
		)
	)
	biscuit.add_task(
		Task.create_task(
			name="Morning walk",
			description="Walk around the neighborhood",
			duration=25,
			priority=3,
			scheduled_start=time(8, 0),
			frequency="daily",
		)
	)
	mochi.add_task(
		Task.create_task(
			name="Medication",
			description="Give Mochi the prescribed medicine",
			duration=5,
			priority=1,
			scheduled_start=time(18, 0),
			frequency="daily",
		)
	)

	scheduler = Scheduler(owner)
	schedule = scheduler.create_daily_schedule()

	print("Today's Schedule")
	print("----------------")
	for task in schedule:
		pet_name = next(
			pet.name
			for pet in owner.pets
			for pet_task in pet.tasks
			if pet_task is task
		)
		start_time = task.scheduled_start.strftime("%I:%M %p")
		print(
			f"{start_time} | {pet_name} | {task.name}: {task.description} "
			f"({task.duration} min, priority {task.priority})"
		)


if __name__ == "__main__":
	main()
