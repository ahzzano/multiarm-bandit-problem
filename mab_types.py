from typing import Protocol
from dataclasses import dataclass
from random import random
import numpy as np 
import pandas as pd

@dataclass
class Arm:
    name: str
    probability: float = 0.5
    default_probability: float = 0.5

    @classmethod
    def new(cls, name: str, probability):
        return Arm(name, probability, probability)

    def play(self) -> bool:
        if random() <= self.probability:
            return True
        else:
            return False

    def set_probability(self, probability: float):
    	self.probability = probability

    def reset(self):
    	self.probability = self.default_probability

class Solver(Protocol):
	def tick(self) -> int:
		...

	def update(self, outcome: bool) -> None:
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

	def tick(self, with_change=False):
		self._ticks += 1
		selected_arm = self._solver.tick()
		result = self._arms[selected_arm].play()
		if with_change:
			print(f'Arm {self._arms[selected_arm].name:<10} Tick {self._ticks:<10}: {result:<5} CHANGE TRIGGERED')
		else:
			print(f'Arm {self._arms[selected_arm].name:<10} Tick {self._ticks:<10}: {result:<5}', end='\r')
		self._solver.update(result)
		self._visits[selected_arm] += 1

		if result:
			self._wins[selected_arm] += 1
		else:
			self._losses[selected_arm] += 1

		self._logs.append(self._arms[selected_arm].name)

	def apply_changes(self, new_probs: list[float]):
		for arm, new_prob in zip(self._arms, new_probs):
			arm.set_probability(new_prob)

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
		df.to_csv(filename)


	def run(self, n=1_000_000, changes: dict[int, list[float]] = dict()):
		self._visits = np.zeros(len(self._arms)).astype(int)
		self._wins = np.zeros(len(self._arms)).astype(int)
		self._losses = np.zeros(len(self._arms)).astype(int)

		for a in self._arms:
			a.reset()

		self._ticks = 0

		np.set_printoptions(precision=3)
	
		for i in range(n):
			a = changes.get(i)
			if a != None:
				self.apply_changes(a)

			self.tick(with_change=a != None)

		p_visits = (self._visits / n) * 100

		print('')
		print(f'visits : {self._visits} : Most Visited: {self._arms[np.argmax(self._visits)].name}')
		print(f'wins   : {self._wins} : Most Wins: {self._arms[np.argmax(self._wins)].name}')
		print(f'losses : {self._losses} : Most Losses: {self._arms[np.argmax(self._losses)].name}')
		print(f'%visits: {p_visits}')

