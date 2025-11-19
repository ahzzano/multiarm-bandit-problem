from mab_types import Arm, MultiArmBandit
from solvers import BasicSolver, EpsilonGreedy

def main():
    arms = [
        Arm.new("A", 0.4),
        Arm.new("B", 0.1),
        Arm.new("C", 0.7),
        Arm.new("D", 0.6),
    ]

    # solver = BasicSolver(len(arms))
    solver = EpsilonGreedy(len(arms), 0.65)
    changes = {
        5_500_000: [0.9, 0.1, 0.1, 0.1]
    }
    mab = MultiArmBandit(arms, solver)
    mab.run(n=50_000_000, changes = changes)

if __name__ == "__main__":
    main()
