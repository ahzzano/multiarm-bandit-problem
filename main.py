from mab_types import BooleanArm, MultiArmBandit, Arm
from solvers import BasicSolver, EpsilonGreedy, UpperConfidenceBound, ThompsonSampling, ExploreOnly, ExploitOnly

def main():
    arms: list[Arm] = [
        BooleanArm("A", 0.5),
        BooleanArm("B", 0.3),
        BooleanArm("C", 0.1),
    ]

    solvers = [
        # BasicSolver(len(arms)),
        ExploreOnly(len(arms)),
        ExploitOnly(len(arms)),
        EpsilonGreedy(len(arms), 0.4),
        UpperConfidenceBound(len(arms), 4),
        ThompsonSampling(len(arms))
    ]

    solver_names = ['ExploreOnly', 'ExploitOnly', 'EpsilonGreedy', 'UCB', 'Thompson']

    for n, s in zip(solver_names, solvers):
        print('Solving...')
        mab = MultiArmBandit(arms, s)
        mab.run(n=1_000_000)

        mab.write_logs(f'results/{n}.txt')
        mab.write_stats(f'results/{n}.csv')

if __name__ == "__main__":
    main()
