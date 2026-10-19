from dataclasses import dataclass, field
from typing import List


@dataclass
class Owner:
	name: str
	address: str

	def add_owner_information(self, name: str, address: str) -> None:
		pass

	def add_pet_information(self, pet: "Pet") -> None:
		pass


@dataclass
class Pet:
	name: str
	age: int
	pet_type: str
	breed: str


@dataclass
class Task:
	name: str
	description: str
	duration: int
	priority: int

	@classmethod
	def create_task(cls) -> "Task":
		pass

	def edit_task(self) -> None:
		pass

	def delete_task(self) -> None:
		pass


@dataclass
class Planner:
	daily_schedule: List[Task] = field(default_factory=list)
	constraints: List[str] = field(default_factory=list)
	priorities: List[str] = field(default_factory=list)
	reasoning: str = ""

	def create_daily_schedule(self) -> List[Task]:
		pass

	def consider_constraints(self) -> None:
		pass

	def consider_priorities(self) -> None:
		pass

	def provide_reasoning(self) -> str:
		pass

	def display(self) -> None:
		pass
