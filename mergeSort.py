import time
from contextlib import contextmanager
from multiprocessing import Manager, Pool

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


def mergesort(array):
    array_length = len(array)

    if array_length <= 1:
        return array

    middle_index = int(array_length / 2)
    left = array[0:middle_index]
    right = array[middle_index:]

    left = mergesort(left)
    right = mergesort(right)

    return merge(left, right)


def mergesort_multiple(results, array):
    results.append(mergesort(array))


def merge_multiple(results, array_part_left, array_part_right):
    results.append(merge(array_part_left, array_part_right))


@contextmanager
def process_pool(size):
    pool = Pool(size)
    yield pool
    pool.close()
    pool.join()


def mergesortMulti(array, process_count):
    # Divide the list in chunks
    step = int(len(array) / process_count)

    manager = Manager()
    results = manager.list()

    with process_pool(size=process_count) as pool:
        for n in range(process_count):
            if n < process_count - 1:
                chunk = array[n * step : (n + 1) * step]
            
            else:
                chunk = array[n * step:]

            pool.apply_async(mergesort_multiple, (results, chunk))


    while len(results) > 1:
        with process_pool(size=process_count) as pool:
            pool.apply_async(merge_multiple, (results, results.pop(0), results.pop(0)))

    return results[0]



if __name__ == '__main__':
    arr = [3, 6, 1, 9, 4, 2, 8, 7, 5]

    start_time = time.time()
    result = mergesortMulti(arr, 4)
    print(f"Time multi processes: {time.time() - start_time}")
    print(result)

    start_time = time.time()
    print(mergesort(arr))
    print(f"Time mono process: {time.time() - start_time}")