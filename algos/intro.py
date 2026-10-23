def sort(arr):
    comparisons = 0
    writes = 0

    def insertion_sort(start, end):
        nonlocal comparisons, writes
        for i in range(start + 1, end + 1):
            key = arr[i]
            j = i - 1
            while j >= start:
                comparisons += 1
                if arr[j] > key:
                    arr[j + 1] = arr[j]
                    writes += 1
                    j -= 1
                else:
                    break
            arr[j + 1] = key
            writes += 1

    def heapify(n, i, start):
        nonlocal comparisons, writes
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2
        
        if left < n:
            comparisons += 1
            if arr[start + left] > arr[start + largest]:
                largest = left
                
        if right < n:
            comparisons += 1
            if arr[start + right] > arr[start + largest]:
                largest = right
                
        if largest != i:
            arr[start + i], arr[start + largest] = arr[start + largest], arr[start + i]
            writes += 2
            heapify(n, largest, start)

    def heap_sort(start, end):
        nonlocal writes
        n = end - start + 1
        for i in range(n // 2 - 1, -1, -1):
            heapify(n, i, start)
        for i in range(n - 1, 0, -1):
            arr[start + i], arr[start] = arr[start], arr[start + i]
            writes += 2
            heapify(i, 0, start)

    def median_of_three(low, mid, high):
        nonlocal comparisons
        comparisons += 1
        if arr[low] < arr[mid]:
            comparisons += 1
            if arr[mid] < arr[high]:
                return mid
            comparisons += 1
            if arr[low] < arr[high]:
                return high
            return low
        else:
            comparisons += 1
            if arr[low] < arr[high]:
                return low
            comparisons += 1
            if arr[mid] < arr[high]:
                return high
            return mid

    def partition(low, high):
        nonlocal comparisons, writes
        mid = low + (high - low) // 2
        pivot_idx = median_of_three(low, mid, high)
        
        if pivot_idx != high:
            arr[pivot_idx], arr[high] = arr[high], arr[pivot_idx]
            writes += 2
        
        pivot = arr[high]
        i = low - 1
        for j in range(low, high):
            comparisons += 1
            if arr[j] <= pivot:
                i += 1
                if i != j:
                    arr[i], arr[j] = arr[j], arr[i]
                    writes += 2
        
        if i + 1 != high:
            arr[i + 1], arr[high] = arr[high], arr[i + 1]
            writes += 2
            
        return i + 1

    def intro_sort(start, end, max_depth):
        size = end - start + 1
        if size <= 16:
            insertion_sort(start, end)
            return
            
        if max_depth == 0:
            heap_sort(start, end)
            return
            
        pivot = partition(start, end)
        if pivot - 1 > start:
            intro_sort(start, pivot - 1, max_depth - 1)
        if pivot + 1 < end:
            intro_sort(pivot + 1, end, max_depth - 1)

    if arr and len(arr) > 1:
        max_depth = 2 * (len(arr).bit_length() - 1)
        intro_sort(0, len(arr) - 1, max_depth)
        
    return comparisons, writes