"""FizzBuzz with configurable divisors."""
import sys
from typing import List, Tuple


def fizzbuzz(n: int, rules: List[Tuple[int, str]] = None) -> List[str]:
    """Generate FizzBuzz sequence with custom rules.

    Args:
        n: Upper bound (inclusive)
        rules: List of (divisor, label) tuples. Defaults to [(3, 'Fizz'), (5, 'Buzz')]

    Returns:
        List of FizzBuzz results
    """
    if rules is None:
        rules = [(3, 'Fizz'), (5, 'Buzz')]

    results = []
    for i in range(1, n + 1):
        out = ''.join(label for div, label in rules if i % div == 0)
        results.append(out or str(i))
    return results


def print_fizzbuzz(n: int, rules=None):
    for item in fizzbuzz(n, rules):
        print(item)


if __name__ == "__main__":
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 100
    print_fizzbuzz(count)
