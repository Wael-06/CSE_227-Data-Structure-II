def sort(arr):
    comparisons = 0
    writes = 0
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            comparisons += 1
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j                 + 1], arr[j]
                writes += 2
                swapped = True
        if not swapped:
            break
    return comparisons, writes
