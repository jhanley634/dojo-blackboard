"""
Recursively solve the famous Towers of Hanoi problem.
"""

Peg = str


def hanoi(n: int, source: Peg, target: Peg, aux: Peg) -> None:
    if n == 0:
        return  # base case

    hanoi(n - 1, source, aux, target)

    print(f"Move disk {n} from {source} to {target}")

    hanoi(n - 1, aux, target, source)


if __name__ == "__main__":
    hanoi(3, "A", "C", "B")
