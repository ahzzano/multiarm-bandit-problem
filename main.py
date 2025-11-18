from dataclasses import dataclass
from random import random

@dataclass
class Arm:
    name: str
    probability: float = 0.5

    @classmethod
    def new(cls, name: str, probability):
        return Arm(name, probability)

    def play(self) -> bool:
        if random() <= self.probability:
            return True
        else:
            return False

def main():
    arms = [
        Arm.new("A", 0.5),
        Arm.new("B", 0.3),
        Arm.new("C", 0.2),
    ]

    print("Hello from multiarm-bandit-problem!")


if __name__ == "__main__":
    main()
