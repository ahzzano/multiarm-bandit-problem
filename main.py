from mab_types import Arm, MultiArmBandit
from solvers import BasicSolver, EpsilonGreedy, UpperConfidenceBound, ThompsonSampling

def main():
    arms = [
        Arm.new("A", 0.5),
        Arm.new("B", 0.45),
    ]

    # solver = BasicSolver(len(arms))
    # solver = EpsilonGreedy(len(arms), 0.4)
    # solver = UpperConfidenceBound(len(arms), 4)
    solver = ThompsonSampling(len(arms))

    mab = MultiArmBandit(arms, solver)
    mab.run(n=1_500_000, changes = {
        # 250_000: [0.05, 0.9]
        })

if __name__ == "__main__":
    main()
