
def sort(arr):
  n = len(arr)
  comparisons = 0
  writes = 0
  
  for i in range(1, n):
      key = arr[i]
      j = i - 1
      
      while j >= 0:
          comparisons += 1
          if arr[j] > key:
              arr[j + 1] = arr[j]
              writes += 1
              j -= 1
          else:
              break
      
      arr[j + 1] = key
      writes +=1
  
  return comparisons, writes