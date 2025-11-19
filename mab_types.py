from typing import Protocol
from dataclasses import dataclass
from random import random
import numpy as np 

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

    def set_probability(self, probability: float):
    	self.probability = probability

class Solver(Protocol):
	def tick(self) -> int:
		...

	def update(self, outcome: bool) -> None:
		...

class MultiArmBandit:
	_arms: list[Arm]
	_solver: Solver
	_ticks = 0

	def __init__(self, arms: list[Arm], solver: Solver):
		self._arms = arms
		self._solver = solver
		self._visits = np.zeros(len(arms))
		self._wins = np.zeros(len(arms))
		self._losses = np.zeros(len(arms))

	def get_ticks(self):
		return self._ticks

	def tick(self):
		self._ticks += 1
		selected_arm = self._solver.tick()
		result = self._arms[selected_arm].play()
		print(f'Arm {self._arms[selected_arm].name:<10} Tick {self._ticks:<10}: {result:<5}', end='\r')
		self._solver.update(result)
		self._visits[selected_arm] += 1

		if result:
			self._wins[selected_arm] += 1
		else:
			self._losses[selected_arm] += 1

	def run(self, n=1_000_000):
		self._visits = np.zeros(len(self._arms))
		self._wins = np.zeros(len(self._arms))
		self._losses = np.zeros(len(self._arms))
		self._ticks = 0

		for i in range(n):
			self.tick()
		print('')
		print(f'visits : {self._visits}')
		print(f'wins   : {self._wins}')
		print(f'losses : {self._losses}')

