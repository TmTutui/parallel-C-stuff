import multiprocessing, time

def merge(left, right):
    result = []
    i, j = 0, 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result += left[i:]
    result += right[j:]
    return result

def mergesortMulti(arr):
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = arr[:mid]
    right = arr[mid:]

    with multiprocessing.Pool() as pool:
        left = pool.apply_async(mergesortMulti, [left])
        right = pool.apply_async(mergesortMulti, [right])
        left = left.get()
        right = right.get()
    
    return merge(left, right)


if __name__ == '__main__':
    arr = [3, 6, 1, 9, 4, 2, 8, 7, 5]

    start_time = time.time()
    result = mergesortMulti(arr)
    print(f"Time multi processes: {time.time() - start_time}")
    print(result)

    start_time = time.time()
    quicksort(arr)
    print(f"Time mono process: {time.time() - start_time}")