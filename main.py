from mab_types import Arm, MultiArmBandit
from solvers import BasicSolver, EpsilonGreedy, UpperConfidenceBound, ThompsonSampling, ExploreOnly, ExploitOnly

def main():
    arms = [
        Arm.new("A", 0.5),
        Arm.new("B", 0.45),
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
        mab.run(n=10_000_000, changes = {
            # 250_000: [0.05, 0.9]
        })

        mab.write_logs(f'results/{n}.txt')
        mab.write_stats(f'results/{n}.csv')

if __name__ == "__main__":
    main()
