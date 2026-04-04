"""
Binary Search Algorithm Implementation

This module provides an efficient implementation of the binary search algorithm
with comprehensive error handling and type validation.

The binary search algorithm works by repeatedly dividing the search interval
in half. It begins with an interval covering the whole array and if the value
of the search key is less than the item in the middle, narrow the interval
to the lower half. Otherwise, narrow it to the upper half.

Time Complexity: O(log n)
Space Complexity: O(1) for iterative, O(log n) for recursive

Author: AI Assistant
"""

from typing import List, Optional, Union, TypeVar
from dataclasses import dataclass
from enum import Enum

T = TypeVar('T')


class SearchResult(Enum):
    """Enumeration representing the result status of a search operation."""
    FOUND = "found"
    NOT_FOUND = "not_found"
    INVALID_INPUT = "invalid_input"


@dataclass
class BinarySearchResult:
    """Data class to encapsulate the result of a binary search operation.

    Attributes:
        status: The result status of the search
        index: The index where the target was found, or -1 if not found
        comparisons: The number of comparisons made during the search
        target: The value that was searched for
    """
    status: SearchResult
    index: int
    comparisons: int
    target: Optional[Union[int, float, str]]


def binary_search(
    arr: List[Union[int, float, str]],
    target: Union[int, float, str],
    low: Optional[int] = None,
    high: Optional[int] = None,
    reverse: bool = False,
) -> BinarySearchResult:
    """
    Perform a binary search on a sorted array to find the target element.

    This implementation supports both ascending and descending sorted arrays,
    and provides detailed search results including the number of comparisons
    made during the search process.

    Args:
        arr: A sorted list of comparable elements (integers, floats, or strings)
        target: The element to search for in the array
        low: Optional lower bound index (defaults to 0)
        high: Optional upper bound index (defaults to len(arr) - 1)
        reverse: If True, assumes the array is sorted in descending order

    Returns:
        BinarySearchResult: An object containing the search status, index,
            number of comparisons, and the target value

    Raises:
        TypeError: If the array contains non-comparable elements

    Examples:
        >>> result = binary_search([1, 2, 3, 4, 5], 3)
        >>> result.status == SearchResult.FOUND
        True
        >>> result.index
        2
    """
    if not isinstance(arr, list):
        return BinarySearchResult(
            status=SearchResult.INVALID_INPUT,
            index=-1,
            comparisons=0,
            target=target
        )

    if len(arr) == 0:
        return BinarySearchResult(
            status=SearchResult.NOT_FOUND,
            index=-1,
            comparisons=0,
            target=target
        )

    if low is None:
        low = 0
    if high is None:
        high = len(arr) - 1

    comparisons = 0

    while low <= high:
        mid = low + (high - low) // 2
        comparisons += 1

        if arr[mid] == target:
            return BinarySearchResult(
                status=SearchResult.FOUND,
                index=mid,
                comparisons=comparisons,
                target=target
            )

        if reverse:
            if arr[mid] > target:
                low = mid + 1
            else:
                high = mid - 1
        else:
            if arr[mid] < target:
                low = mid + 1
            else:
                high = mid - 1

    return BinarySearchResult(
        status=SearchResult.NOT_FOUND,
        index=-1,
        comparisons=comparisons,
        target=target
    )


def binary_search_recursive(
    arr: List[Union[int, float, str]],
    target: Union[int, float, str],
    low: int = 0,
    high: Optional[int] = None,
    comparisons: int = 0,
) -> BinarySearchResult:
    """
    Recursive implementation of binary search algorithm.

    This variant uses recursion instead of iteration, which may be more
    intuitive but uses O(log n) stack space.

    Args:
        arr: A sorted list of comparable elements
        target: The element to search for
        low: Lower bound index (default: 0)
        high: Upper bound index (default: len(arr) - 1)
        comparisons: Running count of comparisons (used internally)

    Returns:
        BinarySearchResult: Search result with status and metadata
    """
    if high is None:
        high = len(arr) - 1

    if low > high:
        return BinarySearchResult(
            status=SearchResult.NOT_FOUND,
            index=-1,
            comparisons=comparisons,
            target=target
        )

    mid = low + (high - low) // 2
    comparisons += 1

    if arr[mid] == target:
        return BinarySearchResult(
            status=SearchResult.FOUND,
            index=mid,
            comparisons=comparisons,
            target=target
        )
    elif arr[mid] < target:
        return binary_search_recursive(arr, target, mid + 1, high, comparisons)
    else:
        return binary_search_recursive(arr, target, low, mid - 1, comparisons)


if __name__ == "__main__":
    # Example usage demonstrating the binary search functionality
    sorted_array = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25]

    # Search for existing element
    result = binary_search(sorted_array, 13)
    print(f"Search for 13: {result.status.value}, index={result.index}, comparisons={result.comparisons}")

    # Search for non-existing element
    result = binary_search(sorted_array, 14)
    print(f"Search for 14: {result.status.value}, index={result.index}, comparisons={result.comparisons}")

    # Recursive search
    result = binary_search_recursive(sorted_array, 7)
    print(f"Recursive search for 7: {result.status.value}, index={result.index}, comparisons={result.comparisons}")
