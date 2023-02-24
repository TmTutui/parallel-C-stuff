import multiprocessing
import time

def quicksortMulti(arr):
    if len(arr) <= 1:
        return arr

    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]

    with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
        return pool.map(quicksortMulti, [left, right]) + middle

def quicksort(arr):
    if len(arr) <= 1:
        return arr

    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    
    return quicksort(left) + quicksort(right) + middle

if __name__ == '__main__':
    arr = [3, 6, 1, 9, 4, 2, 8, 7, 5]

    multiprocessing.set_start_method('spawn')

    start_time = time.time()
    result = quicksortMulti(arr)
    print(f"Time multi processes: {time.time() - start_time}")
    print(result)

    start_time = time.time()
    quicksort(arr)
    print(f"Time mono process: {time.time() - start_time}")

