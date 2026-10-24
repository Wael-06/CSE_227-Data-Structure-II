def sort(arr):
  comparisons = 0
  writes = 0

  def heapify(a,hs,i):
    nonlocal comparisons,writes
    l=2*i+1
    r=2*i+2
    largest=i

    if(l<hs):
      comparisons+=1
      if(a[l]>a[largest]):
        largest=l
      

    if(r<hs):
      comparisons+=1
      if(a[r]>a[largest]):
        largest=r
      

    if(largest!=i):
      a[i],a[largest]=a[largest],a[i]
      writes+=2
      heapify(a,hs,largest)

  def build_heap(a):
    heap_size=len(a)
    start=heap_size//2-1
    for i in range(start,-1,-1):
      heapify(a,heap_size,i)

  def heapsort(a):
    nonlocal writes
    build_heap(a)
    heap_size=len(a)
    for i in range(len(a)-1,0,-1):
      a[0],a[i]=a[i],a[0]
      writes+=2
      heap_size-=1
      heapify(a,heap_size,0)

  heapsort(arr)
  return comparisons, writes    
