"""
Utility functions for common operations.

This module provides a collection of utility functions including
string manipulation, list operations, and mathematical computations
designed for general-purpose use across the project.
"""

from typing import List, Optional, Any, Callable
from functools import reduce
import math


def flatten(nested_list: List[Any], depth: int = -1) -> List[Any]:
    """
    Recursively flatten a nested list structure.

    Args:
        nested_list: A potentially nested list to flatten
        depth: Maximum depth to flatten (-1 for unlimited)

    Returns:
        A flattened list containing all elements from the nested structure
    """
    result = []
    for item in nested_list:
        if isinstance(item, list) and depth != 0:
            result.extend(flatten(item, depth - 1 if depth > 0 else -1))
        else:
            result.append(item)
    return result


def chunk(lst: List[Any], size: int) -> List[List[Any]]:
    """Split a list into chunks of specified size."""
    return [lst[i:i + size] for i in range(0, len(lst), size)]


def unique(lst: List[Any], key: Optional[Callable] = None) -> List[Any]:
    """
    Return unique elements from a list while preserving order.

    Args:
        lst: Input list
        key: Optional function to extract comparison key

    Returns:
        List with duplicates removed, preserving first occurrence order
    """
    seen = set()
    result = []
    for item in lst:
        k = key(item) if key else item
        if k not in seen:
            seen.add(k)
            result.append(item)
    return result


def moving_average(data: List[float], window: int) -> List[float]:
    """
    Calculate the moving average of a numerical sequence.

    Args:
        data: List of numerical values
        window: Size of the moving window

    Returns:
        List of moving average values
    """
    if window <= 0:
        raise ValueError("Window size must be positive")
    if window > len(data):
        return [sum(data) / len(data)] if data else []

    result = []
    window_sum = sum(data[:window])
    result.append(window_sum / window)

    for i in range(window, len(data)):
        window_sum += data[i] - data[i - window]
        result.append(window_sum / window)

    return result


def percentile(data: List[float], p: float) -> float:
    """
    Calculate the p-th percentile of a dataset.

    Args:
        data: List of numerical values
        p: Percentile value (0-100)

    Returns:
        The p-th percentile value
    """
    if not data:
        raise ValueError("Cannot calculate percentile of empty dataset")
    if not 0 <= p <= 100:
        raise ValueError("Percentile must be between 0 and 100")

    sorted_data = sorted(data)
    k = (len(sorted_data) - 1) * p / 100
    f = math.floor(k)
    c = math.ceil(k)

    if f == c:
        return sorted_data[int(k)]

    return sorted_data[f] * (c - k) + sorted_data[c] * (k - f)


def compose(*functions: Callable) -> Callable:
    """
    Compose multiple functions into a single function.

    Functions are applied right-to-left, matching mathematical notation.

    Args:
        *functions: Functions to compose

    Returns:
        A new function that is the composition of all input functions
    """
    return reduce(lambda f, g: lambda *args, **kwargs: f(g(*args, **kwargs)), functions)
