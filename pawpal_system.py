from dataclasses import dataclass, field
from datetime import date, time, timedelta
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
	due_date: Optional[date] = None

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
		due_date: Optional[date] = None,
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
			due_date,
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
	conflict_warnings: List[str] = field(default_factory=list)

	def filter_tasks(
		self,
		completed: Optional[bool] = None,
		pet_name: Optional[str] = None,
	) -> List[Task]:
		"""Return owner tasks matching the optional completion and pet-name filters.

		Pet names match exactly but are case-insensitive. If both filters are
		provided, a task must match both; omitting them returns all owner tasks.
		"""
		normalized_pet_name = pet_name.casefold() if pet_name is not None else None
		return [
			task
			for pet in self.owner.pets
			if normalized_pet_name is None
			or pet.name.casefold() == normalized_pet_name
			for task in pet.tasks
			if completed is None or task.completed is completed
		]

	def sort_by_time(self, tasks: Optional[List[Task]] = None) -> List[Task]:
		"""Return tasks ordered by scheduled start time.

		When tasks are omitted, all owner tasks are sorted. Unscheduled tasks go
		last, and higher priority comes first when start times are equal.
		"""
		tasks_to_sort = self.owner.get_all_tasks() if tasks is None else tasks
		return sorted(
			tasks_to_sort,
			key=lambda task: (
				task.scheduled_start is None,
				task.scheduled_start or time.max,
				-task.priority,
			),
		)

	def detect_conflicts(self, tasks: Optional[List[Task]] = None) -> List[str]:
		"""Return warnings for overlapping scheduled task intervals.

		Each interval uses the task's start time and duration. Tasks without a
		start time are skipped. If tasks are omitted, the current daily schedule
		is checked; overlaps produce warnings and do not raise errors.
		"""
		tasks_to_check = self.daily_schedule if tasks is None else tasks
		intervals = []
		for task in tasks_to_check:
			if task.scheduled_start is None:
				continue
			start_seconds = (
				task.scheduled_start.hour * 3600
				+ task.scheduled_start.minute * 60
				+ task.scheduled_start.second
			)
			intervals.append(
				(task, start_seconds, start_seconds + task.duration * 60)
			)

		warnings = []
		for index, (task, start, end) in enumerate(intervals):
			for other_task, other_start, other_end in intervals[index + 1 :]:
				if start < other_end and other_start < end:
					warnings.append(
						f"Warning: '{task.name}' overlaps with '{other_task.name}'."
					)
		return warnings

	def create_daily_schedule(self) -> List[Task]:
		"""Build today's schedule from incomplete, currently due owner tasks.

		Tasks without a due date are included. Future-dated tasks are held back.
		The returned tasks are ordered by time, and overlap warnings are stored
		in ``conflict_warnings``.
		"""
		today = date.today()
		tasks = [
			task
			for task in self.owner.get_all_tasks()
			if not task.completed and (task.due_date is None or task.due_date <= today)
		]
		self.daily_schedule = self.sort_by_time(tasks)
		self.conflict_warnings = self.detect_conflicts(self.daily_schedule)
		self.reasoning = (
			"Completed tasks are excluded; remaining tasks are ordered by "
			"scheduled time, then descending priority."
		)
		return list(self.daily_schedule)

	def mark_task_completed(self, task: Task) -> None:
		"""Complete an owned task and remove it from the current schedule.

		Daily and weekly tasks receive a fresh occurrence due one or seven days
		from today. Completing an already completed task does not create another
		occurrence. Raises ``ValueError`` if the task is not owned by this owner.
		"""
		pet = next(
			(
				owner_pet
				for owner_pet in self.owner.pets
				if any(owner_task is task for owner_task in owner_pet.tasks)
			),
			None,
		)
		if pet is None:
			raise ValueError("Task does not belong to this owner")
		was_completed = task.completed
		task.completed = True
		self.daily_schedule = [
			scheduled_task
			for scheduled_task in self.daily_schedule
			if scheduled_task is not task
		]

		recurrence_days = {"daily": 1, "weekly": 7}.get(task.frequency.casefold())
		if not was_completed and recurrence_days is not None:
			pet.add_task(
				Task.create_task(
					name=task.name,
					description=task.description,
					duration=task.duration,
					priority=task.priority,
					scheduled_start=task.scheduled_start,
					frequency=task.frequency,
					due_date=date.today() + timedelta(days=recurrence_days),
				)
			)

	def provide_reasoning(self) -> str:
		"""Return the reasoning recorded for the most recent schedule."""
		return self.reasoning
