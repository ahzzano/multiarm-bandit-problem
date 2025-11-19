from mab_types import Arm, MultiArmBandit
from solvers import BasicSolver, EpsilonGreedy

def main():
    arms = [
        Arm.new("A", 0.4),
        Arm.new("B", 0.1),
        Arm.new("C", 0.7),
    ]

    # solver = BasicSolver(len(arms))
    solver = EpsilonGreedy(len(arms), 0.65)
    mab = MultiArmBandit(arms, solver)
    mab.run(n=10_000_000)

if __name__ == "__main__":
    main()
