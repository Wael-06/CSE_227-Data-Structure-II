"""
Hoare QuickSort with Tail-Call optimization.

Optimization:
- Recurse into the smaller partition and loop over the larger partition.
  This bounds QuickSort's call-stack depth to O(log n).
- This does not prevent O(n^2) worst-case running time.

Disclaimer:
- Standard Hoare partitioning using inward-scanning two-pointer swaps.
- Includes median-of-three pivot selection and tail-recursion elimination to guarantee O(log n) call-stack depth.
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
    a,b,c = arr[low], arr[mid], arr[high]
    if (a <= b <= c) or (c <= b <= a):
        return mid
    elif (b <= a <= c) or (c <= a <= b):
        return low
    else:
        return high

  def partition(low, high):
    nonlocal comparisons
    pivot=arr[best_of_three(low, high)]
    i = low - 1
    j = high + 1

    while True:
      i += 1
      while True:
          comparisons += 1
          if not (arr[i] < pivot):
              break
          i += 1
      j -= 1
      while True:
          comparisons += 1
          if not (arr[j] > pivot):
              break
          j -= 1

      if i >= j:
          return j
      
      swap(i, j)

  def quicksort(low, high):

    while (low < high):
      split = partition(low, high)
      left_size = split - low + 1
      right_size = high - split
      
      if (left_size < right_size):
          quicksort(low, split)
          low = split + 1
      else:
          quicksort(split + 1, high)
          high = split

  if (len(arr) > 1):
        quicksort(0, len(arr) - 1)

  return comparisons, writes