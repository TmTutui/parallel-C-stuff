import billiard as multiprocessing


def quicksortMulti(arr):
    if len(arr) <= 1:
        return arr

    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    right = [x for x in arr if x > pivot]

    with multiprocessing.Pool() as pool:
        left, right = pool.map(quicksortMulti, [left, right])
        return left + [pivot] + right

def quicksort(arr):
    if len(arr) <= 1:
        return arr

    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    right = [x for x in arr if x > pivot]
    
    return quicksort(left) + [pivot] + quicksort(right)
