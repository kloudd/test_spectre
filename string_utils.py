"""
String utility functions for common text manipulation operations.

This module provides functions for reversing strings, checking palindromes,
detecting anagrams, and encoding/decoding with a Caesar cipher.
"""

from collections import Counter


def reverse_string(s: str) -> str:
    """
    Reverse a string.

    Args:
        s: The input string to reverse

    Returns:
        The reversed string

    Examples:
        >>> reverse_string("hello")
        'olleh'
        >>> reverse_string("")
        ''
    """
    return s[::-1]


def is_palindrome(s: str, ignore_case: bool = True, ignore_spaces: bool = True) -> bool:
    """
    Check whether a string is a palindrome.

    Args:
        s: The input string to check
        ignore_case: If True, comparison is case-insensitive
        ignore_spaces: If True, spaces are stripped before comparison

    Returns:
        True if the string is a palindrome, False otherwise

    Examples:
        >>> is_palindrome("racecar")
        True
        >>> is_palindrome("A man a plan a canal Panama")
        True
        >>> is_palindrome("hello")
        False
    """
    cleaned = s
    if ignore_spaces:
        cleaned = cleaned.replace(" ", "")
    if ignore_case:
        cleaned = cleaned.lower()
    return cleaned == cleaned[::-1]


def is_anagram(a: str, b: str, ignore_case: bool = True, ignore_spaces: bool = True) -> bool:
    """
    Check whether two strings are anagrams of each other.

    Two strings are anagrams if they contain the same characters
    with the same frequencies.

    Args:
        a: First string
        b: Second string
        ignore_case: If True, comparison is case-insensitive
        ignore_spaces: If True, spaces are ignored

    Returns:
        True if the strings are anagrams, False otherwise

    Examples:
        >>> is_anagram("listen", "silent")
        True
        >>> is_anagram("hello", "world")
        False
    """
    def normalize(s: str) -> str:
        if ignore_spaces:
            s = s.replace(" ", "")
        if ignore_case:
            s = s.lower()
        return s

    return Counter(normalize(a)) == Counter(normalize(b))


def caesar_cipher(text: str, shift: int, decrypt: bool = False) -> str:
    """
    Encode or decode a string using a Caesar cipher.

    Only alphabetic characters are shifted; digits, punctuation, and
    whitespace are left unchanged. The shift wraps around the alphabet.

    Args:
        text: The input text to encode or decode
        shift: Number of positions to shift each letter
        decrypt: If True, shift in the opposite direction to decode

    Returns:
        The encoded or decoded string

    Examples:
        >>> caesar_cipher("hello", 3)
        'khoor'
        >>> caesar_cipher("khoor", 3, decrypt=True)
        'hello'
    """
    if decrypt:
        shift = -shift

    result = []
    for ch in text:
        if ch.isalpha():
            base = ord('A') if ch.isupper() else ord('a')
            shifted = (ord(ch) - base + shift) % 26 + base
            result.append(chr(shifted))
        else:
            result.append(ch)

    return "".join(result)
