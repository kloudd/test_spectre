"""
Tests for utility functions in utils.py.

Covers flatten, chunk, unique, moving_average, and median.
"""

import pytest
from utils import flatten, chunk, unique, moving_average, median


# ── flatten ──────────────────────────────────────────────────────────

class TestFlatten:
    def test_flat_list_unchanged(self):
        assert flatten([1, 2, 3]) == [1, 2, 3]

    def test_single_level_nesting(self):
        assert flatten([1, [2, 3], 4]) == [1, 2, 3, 4]

    def test_deep_nesting(self):
        assert flatten([1, [2, [3, [4, [5]]]]]) == [1, 2, 3, 4, 5]

    def test_empty_list(self):
        assert flatten([]) == []

    def test_nested_empty_lists(self):
        assert flatten([[], [[]], [[], []]]) == []

    def test_depth_limited(self):
        assert flatten([1, [2, [3, [4]]]], depth=1) == [1, 2, [3, [4]]]

    def test_depth_zero_does_nothing(self):
        nested = [1, [2, 3]]
        assert flatten(nested, depth=0) == [1, [2, 3]]

    def test_mixed_types(self):
        assert flatten([1, ["a", [True, [None]]]]) == [1, "a", True, None]


# ── chunk ────────────────────────────────────────────────────────────

class TestChunk:
    def test_even_split(self):
        assert chunk([1, 2, 3, 4], 2) == [[1, 2], [3, 4]]

    def test_uneven_split(self):
        assert chunk([1, 2, 3, 4, 5], 2) == [[1, 2], [3, 4], [5]]

    def test_chunk_size_larger_than_list(self):
        assert chunk([1, 2], 5) == [[1, 2]]

    def test_chunk_size_one(self):
        assert chunk([1, 2, 3], 1) == [[1], [2], [3]]

    def test_empty_list(self):
        assert chunk([], 3) == []


# ── unique ───────────────────────────────────────────────────────────

class TestUnique:
    def test_removes_duplicates(self):
        assert unique([1, 2, 2, 3, 3, 3]) == [1, 2, 3]

    def test_preserves_order(self):
        assert unique([3, 1, 2, 1, 3]) == [3, 1, 2]

    def test_empty_list(self):
        assert unique([]) == []

    def test_all_same(self):
        assert unique([7, 7, 7]) == [7]

    def test_with_key_function(self):
        data = ["apple", "APPLE", "Banana", "banana"]
        result = unique(data, key=str.lower)
        assert result == ["apple", "Banana"]

    def test_strings(self):
        assert unique(["a", "b", "a", "c"]) == ["a", "b", "c"]


# ── moving_average ───────────────────────────────────────────────────

class TestMovingAverage:
    def test_basic(self):
        result = moving_average([1, 2, 3, 4, 5], 3)
        assert len(result) == 3
        assert result[0] == pytest.approx(2.0)
        assert result[1] == pytest.approx(3.0)
        assert result[2] == pytest.approx(4.0)

    def test_window_equals_length(self):
        result = moving_average([10, 20, 30], 3)
        assert result == [pytest.approx(20.0)]

    def test_window_larger_than_data(self):
        result = moving_average([5, 15], 5)
        assert result == [pytest.approx(10.0)]

    def test_empty_data(self):
        assert moving_average([], 3) == []

    def test_invalid_window_raises(self):
        with pytest.raises(ValueError, match="positive"):
            moving_average([1, 2, 3], 0)

    def test_single_element(self):
        result = moving_average([42], 1)
        assert result == [pytest.approx(42.0)]


# ── median ───────────────────────────────────────────────────────────

class TestMedian:
    def test_odd_length(self):
        assert median([3, 1, 2]) == 2

    def test_even_length(self):
        assert median([4, 1, 3, 2]) == pytest.approx(2.5)

    def test_single_element(self):
        assert median([99]) == 99

    def test_two_elements(self):
        assert median([10, 20]) == pytest.approx(15.0)

    def test_already_sorted(self):
        assert median([1, 2, 3, 4, 5]) == 3

    def test_negative_values(self):
        assert median([-5, -1, -3]) == -3

    def test_floats(self):
        assert median([1.5, 2.5, 3.5]) == pytest.approx(2.5)

    def test_empty_raises(self):
        with pytest.raises(ValueError, match="empty"):
            median([])

    def test_duplicates(self):
        assert median([5, 5, 5, 5]) == pytest.approx(5.0)
