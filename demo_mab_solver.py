import mab_types
from mab_types import Arm

class BasicSolver:
	def __init__(self, n_arms: int):
		self.n_arms =  n_arms

	def tick(self) -> int:
		return 0