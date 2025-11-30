from mab_types import Arm, BooleanArm, MultiArmBandit, Device
from solvers import BasicSolver, EpsilonGreedy, UpperConfidenceBound, ThompsonSampling, ExploreOnly, ExploitOnly

def main():
    arms: list[Arm] = [
        Device("CPU", 12, 32),
        Device("NCS", 8, 45)
    ]

    solvers = [
        # BasicSolver(len(arms)),
        # ExploreOnly(len(arms)),
        # ExploitOnly(len(arms)),
        # EpsilonGreedy(len(arms), 0.4),
        UpperConfidenceBound(len(arms), 4),
        ThompsonSampling(len(arms))
    ]

    solver_names = ['UCB', 'Thompson']

    for n, s in zip(solver_names, solvers):
        print('Solving...')
        mab = MultiArmBandit(arms, s)
        mab.run(n=500_000)

        mab.write_logs(f'results/{n}.txt')
        mab.write_stats(f'results/{n}.csv')

if __name__ == "__main__":
    main()
