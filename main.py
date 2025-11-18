from mab_types import Arm

def main():
    arms = [
        Arm.new("A", 0.5),
        Arm.new("B", 0.3),
        Arm.new("C", 0.2),
    ]

    print("Hello from multiarm-bandit-problem!")


if __name__ == "__main__":
    main()
