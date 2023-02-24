import billiard as multiprocessing
import time, random

from quickSort import quicksort, quicksortMulti


if __name__ == '__main__':
    arr = [random.random() for _ in range(100)]

    multiprocessing.set_start_method('spawn')

    start_time = time.time()
    result = quicksortMulti(arr)
    print(f"Time multi processes: {time.time() - start_time}")
    print(result)

    start_time = time.time()
    print(quicksort(arr))
    print(f"Time mono process: {time.time() - start_time}")