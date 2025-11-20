from mab_types import Arm, MultiArmBandit
from solvers import BasicSolver, EpsilonGreedy, UpperConfidenceBound

def main():
    arms = [
        Arm.new("A", 0.4),
        Arm.new("B", 0.1),
    ]

    # solver = BasicSolver(len(arms))
    # solver = EpsilonGreedy(len(arms), 0.4)
    solver = UpperConfidenceBound(len(arms), 3)

    mab = MultiArmBandit(arms, solver)
    mab.run(n=500_000, changes = {
        100_000: [0.05, 0.9]
        })

if __name__ == "__main__":
    main()
