def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr


if __name__ == "__main__":
    numbers = [64, 34, 25, 12, 22, 11, 90]
    print("Original:", numbers)
    print("Sorted:  ", insertion_sort(numbers))
