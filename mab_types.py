from numbers import Number
from typing import Protocol
from dataclasses import dataclass
from random import random, uniform
import numpy as np 
import pandas as pd

class BooleanArm:
    def __init__(self, name, probability):
        self._name = name
        self.probability = probability

    @classmethod
    def new(cls, name: str, probability):
        ba = BooleanArm(name, probability)
        return ba

    def pull(self) -> int | float:
        if random() <= self.probability:
            return True
        else:
            return False

    def name(self) -> str:
    	return self._name

class Device:
    def __init__(self, name, a, b):
        self._name = name
        self.a = a 
        self.b = b

    def pull(self) -> int | float:
        return uniform(self.a, self.b)

    def name(self) -> str:
        return self._name

class Arm(Protocol):
	def pull(self) -> int | float:
		...

	def name(self) -> str:
		...

class Solver(Protocol):
	def tick(self) -> int:
		...

	def update(self, outcome: int | float) -> None:
		...

class MultiArmBandit:
	_arms: list[Arm]
	_solver: Solver
	_ticks = 0
	_logs: list[str] = []

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

		result = self._arms[selected_arm].pull()

		print(f'Arm {self._arms[selected_arm].name():<10} Tick {self._ticks:<10}: {result:<5}', end='\r')
		self._solver.update(result)
		self._visits[selected_arm] += 1
		self._wins[selected_arm] += 1    


	def write_logs(self, filename: str):
		with open(filename, 'w+') as f:
			for l in self._logs:
				f.writelines(l+'\n')

	def write_stats(self, filename: str):
		arms = list(map(lambda a: a.name, self._arms))
		data = {
			'arm': arms, 
			'visits': self._visits.tolist(),
			'wins': self._wins.tolist(),
			'losses': self._losses.tolist(),
		}

		df = pd.DataFrame(data)
		df.to_csv(filename, index=False)


	def run(self, n=1_000_000, changes: dict[int, list[float]] = dict()):
		self._visits = np.zeros(len(self._arms)).astype(int)
		self._wins = np.zeros(len(self._arms)).astype(int)
		self._losses = np.zeros(len(self._arms)).astype(int)

		self._ticks = 0

		np.set_printoptions(precision=3)
	
		for i in range(n):
			self.tick()

		p_visits = (self._visits / n) * 100

		print('')
		print(f'visits : {self._visits} : Most Visited: {self._arms[np.argmax(self._visits)].name()}')
		print(f'scores   : {self._wins} : Most Wins: {self._arms[np.argmax(self._wins)].name()}')
		print(f'%visits: {p_visits}')

