from dataclasses import dataclass, field
from datetime import time
from typing import List, Optional


@dataclass
class Owner:
	name: str
	address: str
	pets: List["Pet"] = field(default_factory=list)

	def add_owner_information(self, name: str, address: str) -> None:
		self.name = name
		self.address = address

	def add_pet_information(self, pet: "Pet") -> None:
		if pet not in self.pets:
			self.pets.append(pet)


@dataclass
class Pet:
	name: str
	age: int
	pet_type: str
	breed: str
	tasks: List["Task"] = field(default_factory=list)

	def add_task(self, task: "Task") -> None:
		if task not in self.tasks:
			self.tasks.append(task)


@dataclass
class Task:
	name: str
	description: str
	duration: int
	priority: int
	scheduled_start: Optional[time] = None

	@classmethod
	def create_task(
		cls, name: str, description: str, duration: int, priority: int
	) -> "Task":
		return cls(name, description, duration, priority)

	def edit_task(
		self, name: str, description: str, duration: int, priority: int
	) -> None:
		self.name = name
		self.description = description
		self.duration = duration
		self.priority = priority

	def delete_task(self, pet: "Pet") -> None:
		if self in pet.tasks:
			pet.tasks.remove(self)


@dataclass
class Planner:
	daily_schedule: List[Task] = field(default_factory=list)
	constraints: List[str] = field(default_factory=list)
	priorities: List[str] = field(default_factory=list)
	reasoning: str = ""

	def create_daily_schedule(self) -> List[Task]:
		return list(self.daily_schedule)

	def consider_constraints(self) -> None:
		pass

	def consider_priorities(self) -> None:
		pass

	def provide_reasoning(self) -> str:
		return self.reasoning

	def display(self) -> None:
		pass
