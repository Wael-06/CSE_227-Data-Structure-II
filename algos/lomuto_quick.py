"""
LLVM-inspired Lomuto QuickSort originally from Lomcyc paper with Tail-Call & Median-of-Three.

Partition optimization inspired by LLVM libc:
- For every element before the pivot, perform an unconditional swap.
- Advance the boundary with `left += int(is_less)` instead of an explicit
  conditional around the boundary update.
- This reduces data-dependent control flow in the source algorithm, but
  Python does not guarantee machine-level branchless execution.
- Unconditional swaps cause more writes; that trade-off is intentional.

Optimizations:
- Best-of-three (median-of-three) pivot selection avoids O(n^2) behavior on sorted arrays.
- Recurse into the smaller partition and iterate over the larger one, keeping
  auxiliary call-stack usage bounded to O(log n).

Disclaimer:
- Uses unconditional swaps and arithmetic boundary updates (`left += int(is_less)`) to minimize branching.
- Native branchless execution (`cmov`/`setl`) requires C++ compiler code generation and is not guaranteed in CPython.
- LLVM libc implementation: https://github.com/llvm/llvm-project/blob/main/libc/src/stdlib/quick_sort.h
"""


def sort(arr):
    comparisons = 0
    writes = 0

    def swap(i, j):
        nonlocal writes
        arr[i], arr[j] = arr[j], arr[i]
        writes += 2

    def best_of_three(low, high):
        mid = low + (high - low) // 2
        a, b, c = arr[low], arr[mid], arr[high]
        if (a <= b <= c) or (c <= b <= a):
            return mid
        elif (b <= a <= c) or (c <= a <= b):
            return low
        else:
            return high

    def partition(low, high):
        nonlocal comparisons

        pivot_idx = best_of_three(low, high)
        swap(pivot_idx, high)

        pivot = arr[high]
        left = low
        right = low

        while right < high:
            comparisons += 1
            is_less = arr[right] < pivot

            swap(left, right)

            left += int(is_less)
            right += 1

        swap(left, high)
        return left

    def quicksort(low, high):
        while low < high:
            pivot_index = partition(low, high)

            left_size = pivot_index - low
            right_size = high - pivot_index

            if left_size < right_size:
                quicksort(low, pivot_index - 1)
                low = pivot_index + 1
            else:
                quicksort(pivot_index + 1, high)
                high = pivot_index - 1

    if len(arr) > 1:
        quicksort(0, len(arr) - 1)

    return comparisons, writes