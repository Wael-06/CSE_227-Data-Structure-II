import random

def sort(arr):
  comparisons = 0
  writes = 0

  def swap(i, j):
    nonlocal writes
    arr[i], arr[j] = arr[j], arr[i]
    writes += 2

  def quicksort(low, high):
    nonlocal comparisons

    if low < high:

      pivot = random.randint(low, high)
      swap(pivot, high)
      i = low - 1

      for j in range(low, high):
        comparisons += 1

        if arr[j] <= arr[high]:
          i += 1
          swap(i, j)
          
      swap(i + 1, high)
      pivot_index = i + 1

      quicksort(low, pivot_index - 1)
      quicksort(pivot_index + 1, high)

  if len(arr) > 1:
    quicksort(0, len(arr) - 1)

  return comparisons, writes