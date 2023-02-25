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


def mergesort(arr):
    length = len(arr)

    if length <= 1:
        return arr

    middle_index = length // 2
    left = arr[0:middle_index]
    right = arr[middle_index:]

    left = mergesort(left)
    right = mergesort(right)

    return merge(left, right)


def mergesort_multiple(results, arr):
    results.append(mergesort(arr))


def merge_multiple(results, arr_part_left, arr_part_right):
    results.append(merge(arr_part_left, arr_part_right))


@contextmanager
def process_pool(size):
    pool = Pool(size)
    yield pool
    pool.close()
    pool.join()


def mergesortMulti(arr, nProcessors):
    # Divide the list in chunks
    step = len(arr) // nProcessors

    manager = Manager()
    results = manager.list()

    with process_pool(size=nProcessors) as pool:
        for n in range(nProcessors):
            if n < nProcessors - 1:
                chunk = arr[n * step : (n + 1) * step]
            
            else:
                chunk = arr[n * step:]

            pool.apply_async(mergesort_multiple, (results, chunk))


    while len(results) > 1:
        with process_pool(size=nProcessors) as pool:
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