from dataclasses import dataclass, field
from datetime import time
from typing import List, Optional


@dataclass
class Owner:
	name: str
	address: str
	pets: List["Pet"] = field(default_factory=list)

	def add_owner_information(self, name: str, address: str) -> None:
		"""Update the owner's name and address."""
		self.name = name
		self.address = address

	def add_pet_information(self, pet: "Pet") -> None:
		"""Add a pet to this owner's pets if not already present."""
		if pet not in self.pets:
			self.pets.append(pet)

	def get_all_tasks(self) -> List["Task"]:
		"""Return the tasks belonging to all of this owner's pets."""
		return [task for pet in self.pets for task in pet.tasks]


@dataclass
class Pet:
	name: str
	age: int
	pet_type: str
	breed: str
	tasks: List["Task"] = field(default_factory=list)

	def add_task(self, task: "Task") -> None:
		"""Add a care task to this pet if not already present."""
		if task not in self.tasks:
			self.tasks.append(task)


@dataclass
class Task:
	name: str
	description: str
	duration: int
	priority: int
	scheduled_start: Optional[time] = None
	frequency: str = "once"
	completed: bool = False

	@classmethod
	def create_task(
		cls,
		name: str,
		description: str,
		duration: int,
		priority: int,
		scheduled_start: Optional[time] = None,
		frequency: str = "once",
		completed: bool = False,
	) -> "Task":
		"""Create a task with its care and scheduling details."""
		return cls(
			name,
			description,
			duration,
			priority,
			scheduled_start,
			frequency,
			completed,
		)

	def edit_task(
		self, name: str, description: str, duration: int, priority: int
	) -> None:
		"""Replace this task's name, description, duration, and priority."""
		self.name = name
		self.description = description
		self.duration = duration
		self.priority = priority

	def delete_task(self, pet: "Pet") -> None:
		"""Remove this task from the given pet's task list."""
		if self in pet.tasks:
			pet.tasks.remove(self)


@dataclass
class Scheduler:
	owner: Owner
	daily_schedule: List[Task] = field(default_factory=list)
	reasoning: str = ""

	def create_daily_schedule(self) -> List[Task]:
		"""Build and return an ordered schedule from the owner's tasks."""
		tasks = self.owner.get_all_tasks()
		self.daily_schedule = sorted(
			(task for task in tasks if not task.completed),
			key=lambda task: (
				task.scheduled_start is None,
				task.scheduled_start or time.max,
				-task.priority,
			),
		)
		self.reasoning = (
			"Completed tasks are excluded; remaining tasks are ordered by "
			"scheduled time, then descending priority."
		)
		return list(self.daily_schedule)

	def mark_task_completed(self, task: Task) -> None:
		"""Mark an owned task complete and remove it from the current schedule."""
		if not any(owner_task is task for owner_task in self.owner.get_all_tasks()):
			raise ValueError("Task does not belong to this owner")
		task.completed = True
		self.daily_schedule = [
			scheduled_task
			for scheduled_task in self.daily_schedule
			if scheduled_task is not task
		]

	def provide_reasoning(self) -> str:
		"""Return the reasoning recorded for the most recent schedule."""
		return self.reasoning
