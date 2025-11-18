from mab_types import Arm, MultiArmBandit
from solvers import BasicSolver

def main():
    arms = [
        Arm.new("A", 0.5),
        Arm.new("B", 0.3),
        Arm.new("C", 0.2),
    ]

    solver = BasicSolver(len(arms))
    mab = MultiArmBandit(arms, solver)
    mab.run()

    print("Hello from multiarm-bandit-problem!")

if __name__ == "__main__":
    main()
