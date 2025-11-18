from dataclasses import dataclass

@dataclass
class Arm:
    name: str
    probability: float = 0.5

    @classmethod
    def new(cls, name: str, probability):
        return Arm(name, probability)

def main():
    arms = [
        Arm.new("A", 0.5),
        Arm.new("B", 0.3),
        Arm.new("C", 0.2),
    ]

    print("Hello from multiarm-bandit-problem!")


if __name__ == "__main__":
    main()
