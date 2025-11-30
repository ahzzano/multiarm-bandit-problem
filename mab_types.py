from numbers import Number
from typing import Protocol
from dataclasses import dataclass
from random import random
import numpy as np 
import pandas as pd


class BooleanArm:
    _name: str
    probability: float = 0.5

    @classmethod
    def new(cls, name: str, probability):
        ba = BooleanArm()
        ba._name = name 
        ba.probability = probability
        return ba

    def pull(self) -> Number:
        if random() <= self.probability:
            return True
        else:
            return False

    @property
    def name(self) -> str:
    	return self._name

class Arm(Protocol):
	def pull(self) -> Number:
		...

	@property
	def name(self) -> str:
		...

class Solver(Protocol):
	def tick(self) -> int:
		...

	def update(self, outcome: Number) -> None:
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
		print(f'Arm {self._arms[selected_arm].name:<10} Tick {self._ticks:<10}: {result:<5}', end='\r')
		self._solver.update(result)
		self._visits[selected_arm] += 1

		log_string = ''

		if result:
			self._wins[selected_arm] += 1
			log_string = f'{self._arms[selected_arm].name}-win'
		else:
			self._losses[selected_arm] += 1
			log_string = f'{self._arms[selected_arm].name}-loss'

		self._logs.append(log_string)

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
		print(f'visits : {self._visits} : Most Visited: {self._arms[np.argmax(self._visits)].name}')
		print(f'wins   : {self._wins} : Most Wins: {self._arms[np.argmax(self._wins)].name}')
		print(f'losses : {self._losses} : Most Losses: {self._arms[np.argmax(self._losses)].name}')
		print(f'%visits: {p_visits}')

