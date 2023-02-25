import time, random

from quickSort import quicksort, callQuickSortMulti
from mergeSort import mergesort, mergesortMulti


if __name__ == '__main__':
    arr = [random.randint(0, 100000) for _ in range(1000000)]
    nProcessors = 4

    print("\n----- Quick Sort -----")

    start_time = time.time()
    result = callQuickSortMulti(arr, nProcessors)
    print(f"Time multi processes: {time.time() - start_time}")

    start_time = time.time()
    quicksort(arr)
    print(f"Time mono process: {time.time() - start_time}")

    print("\n")

    print("----- Merge Sort -----")

    start_time = time.time()
    result = mergesortMulti(arr, nProcessors)
    print(f"Time multi processes: {time.time() - start_time}")

    start_time = time.time()
    mergesort(arr)
    print(f"Time mono process: {time.time() - start_time}\n")