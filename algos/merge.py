def sort(arr):
  comparisons = 0
  writes = 0

  def merge(sub, L, R):
    nonlocal comparisons, writes
    i = j = k = 0

    while ((i < len(L)) and (j < len(R))):
      comparisons += 1
      if (L[i] < R[j]):
        sub[k] = L[i]
        i += 1
      else:
        sub[k] = R[j]
        j += 1
      writes += 1
      k += 1

    while (i < len(L)):
      sub[k] = L[i]
      i += 1
      k += 1
      writes += 1

    while (j < len(R)):
      sub[k] = R[j]
      j += 1
      k += 1
      writes += 1
      
  def mergesort(sub):
    if len(sub) > 1:
      mid = len(sub) // 2
      L = sub[:mid]
      R = sub[mid:]
      mergesort(L)
      mergesort(R)

      merge(sub, L, R)

  mergesort(arr)
  return comparisons, writes