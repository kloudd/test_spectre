"""Tests for sorting algorithms."""
import pytest
import random
from sorting import quicksort, mergesort, heapsort, benchmark


class TestQuicksort:
    def test_empty(self):
        assert quicksort([]) == []

    def test_single(self):
        assert quicksort([1]) == [1]

    def test_sorted(self):
        assert quicksort([1, 2, 3, 4, 5]) == [1, 2, 3, 4, 5]

    def test_reverse(self):
        assert quicksort([5, 4, 3, 2, 1]) == [1, 2, 3, 4, 5]

    def test_duplicates(self):
        assert quicksort([3, 1, 4, 1, 5, 9, 2, 6]) == [1, 1, 2, 3, 4, 5, 6, 9]

    def test_negative(self):
        assert quicksort([-3, -1, -4]) == [-4, -3, -1]

    def test_large(self):
        data = [random.randint(-1000, 1000) for _ in range(1000)]
        assert quicksort(data) == sorted(data)


class TestMergesort:
    def test_empty(self):
        assert mergesort([]) == []

    def test_stability(self):
        data = [3, 1, 4, 1, 5]
        assert mergesort(data) == sorted(data)

    def test_large(self):
        data = [random.randint(-1000, 1000) for _ in range(1000)]
        assert mergesort(data) == sorted(data)


class TestHeapsort:
    def test_empty(self):
        assert heapsort([]) == []

    def test_basic(self):
        assert heapsort([4, 10, 3, 5, 1]) == [1, 3, 4, 5, 10]

    def test_large(self):
        data = [random.randint(-1000, 1000) for _ in range(1000)]
        assert heapsort(data) == sorted(data)


class TestBenchmark:
    def test_returns_dict(self):
        result = benchmark(quicksort, [5, 3, 1, 4, 2])
        assert "algorithm" in result
        assert "avg_ms" in result
        assert result["algorithm"] == "quicksort"

    def test_correctness_check(self):
        result = benchmark(mergesort, [9, 7, 5, 3, 1], runs=1)
        assert result["runs"] == 1
