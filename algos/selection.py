def sort(arr):
  comparisons, writes = 0, 0
  for i in range(len(arr)):
    min_index = i
    for j in range(i + 1, len(arr)):
      comparisons += 1
      if arr[j] < arr[min_index]:
        min_index = j

    if min_index != i:
      arr[i], arr[min_index] = arr[min_index], arr[i]
      writes += 2
  return comparisons, writes