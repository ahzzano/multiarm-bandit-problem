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
	def tick(self) -> int:
		...

class MultiArmBandit:
	_arms: list[Arm]
	_solver: Solver
	_ticks = 0

	def __init__(self, arms: list[Arm], solver: Solver):
		self._arms = arms
		self._solver = solver

	def get_ticks(self):
		return self._ticks

	def tick(self):
		self._ticks += 1
		selected_arm = self._solver.tick()
		result = self._arms[selected_arm].play()
		print(f'{self._ticks}: {result}')

	def run(self, n=1_000_000):
		for i in range(n):
			self.tick()
