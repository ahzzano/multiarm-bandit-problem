from typing import Protocol
from dataclasses import dataclass
from random import random

@dataclass
class Arm:
    name: str
    probability: float = 0.5

    @classmethod
    def new(cls, name: str, probability):
        return Arm(name, probability)

    def play(self) -> bool:
        if random() <= self.probability:
            return True
        else:
            return False


class Solver(Protocol):
	def set_arms(arms: list[Arm]):
		...

	def tick() -> str:
		...