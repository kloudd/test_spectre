"""
Sorting algorithm implementations with benchmarking support.
"""
from typing import List, Callable, Any
import time


def quicksort(arr: List[int]) -> List[int]:
    """Quicksort with Lomuto partition scheme."""
    if len(arr) <= 1:
        return arr
    pivot = arr[-1]
    left = [x for x in arr[:-1] if x <= pivot]
    right = [x for x in arr[:-1] if x > pivot]
    return quicksort(left) + [pivot] + quicksort(right)


def mergesort(arr: List[int]) -> List[int]:
    """Stable merge sort implementation."""
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = mergesort(arr[:mid])
    right = mergesort(arr[mid:])
    return _merge(left, right)


def _merge(left: List[int], right: List[int]) -> List[int]:
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


def heapsort(arr: List[int]) -> List[int]:
    """In-place heapsort."""
    arr = arr.copy()
    n = len(arr)

    for i in range(n // 2 - 1, -1, -1):
        _heapify(arr, n, i)

    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        _heapify(arr, i, 0)

    return arr


def _heapify(arr: List[int], n: int, i: int):
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2

    if left < n and arr[left] > arr[largest]:
        largest = left
    if right < n and arr[right] > arr[largest]:
        largest = right

    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        _heapify(arr, n, largest)


def benchmark(sort_fn: Callable, data: List[int], runs: int = 3) -> dict:
    """Benchmark a sorting function."""
    times = []
    for _ in range(runs):
        arr = data.copy()
        start = time.perf_counter()
        result = sort_fn(arr)
        elapsed = time.perf_counter() - start
        times.append(elapsed)
        assert result == sorted(data), f"{sort_fn.__name__} produced incorrect result"

    return {
        "algorithm": sort_fn.__name__,
        "avg_ms": sum(times) / len(times) * 1000,
        "min_ms": min(times) * 1000,
        "max_ms": max(times) * 1000,
        "runs": runs,
    }


if __name__ == "__main__":
    import random
    test_data = [random.randint(0, 10000) for _ in range(5000)]
    for fn in [quicksort, mergesort, heapsort]:
        result = benchmark(fn, test_data)
        print(f"{result['algorithm']:>12}: avg={result['avg_ms']:.2f}ms")
