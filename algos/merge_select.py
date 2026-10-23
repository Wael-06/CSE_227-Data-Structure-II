def selection_sort(sub, comparisons_writes):
    n = len(sub)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            comparisons_writes["comparisons"] += 1
            if sub[j] < sub[min_idx]:
                min_idx = j

        if min_idx != i:
            sub[i], sub[min_idx] = sub[min_idx], sub[i]
            comparisons_writes["writes"] += 2


def sort(arr, threshold=6):
    metrics = {"comparisons": 0, "writes": 0}

    def merge(sub, L, R):
        i = j = k = 0

        while i < len(L) and j < len(R):
            metrics["comparisons"] += 1
            if L[i] < R[j]:
                sub[k] = L[i]
                i += 1
            else:
                sub[k] = R[j]
                j += 1
            metrics["writes"] += 1
            k += 1

        while i < len(L):
            sub[k] = L[i]
            i += 1
            k += 1
            metrics["writes"] += 1

        while j < len(R):
            sub[k] = R[j]
            j += 1
            k += 1
            metrics["writes"] += 1

    def hybrid_mergesort(sub):
        if len(sub) <= threshold:
            selection_sort(sub, metrics)
            return

        mid = len(sub) // 2
        L = sub[:mid]
        R = sub[mid:]

        hybrid_mergesort(L)
        hybrid_mergesort(R)

        merge(sub, L, R)

    hybrid_mergesort(arr)
    return metrics["comparisons"], metrics["writes"]