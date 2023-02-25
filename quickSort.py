import time
from multiprocessing import Process, Pool, Pipe


def quicksortMulti(arr, conn, nProcessors):
    length = len(arr)

    if nProcessors <= 0 or length <= 1:
        conn.send(quicksort(arr))
        conn.close()
        return

    pivot = arr.pop(length//2)

    leftSide = [x for x in arr if x < pivot]
    rightSide = [x for x in arr if x >= pivot]

    pconnLeft, cconnLeft = Pipe()

    leftProc = Process(target=quicksortMulti, args=(leftSide, cconnLeft, nProcessors - 1))
    
    pconnRight, cconnRight = Pipe()
    rightProc = Process(target=quicksortMulti, args=(rightSide, cconnRight, nProcessors - 1))

    leftProc.start()
    rightProc.start()

    conn.send(pconnLeft.recv() + [pivot] + pconnRight.recv())
    conn.close()

    leftProc.join()
    rightProc.join()


def callQuickSortMulti(arr, nProcessors):
    pconn, cconn = Pipe()
    
    p = Process(target=quicksortMulti, args=(arr, cconn, nProcessors))
    p.start()
    
    result = pconn.recv()
    p.join()

    return result

def quicksort(arr):
    length = len(arr)

    if length <= 1:
        return arr

    pivot = arr.pop(length//2)
    left = [x for x in arr if x < pivot]
    right = [x for x in arr if x >= pivot]
    
    return quicksort(left) + [pivot] + quicksort(right)



if __name__ == '__main__':
    arr = [3, 6, 1, 9, 4, 2, 8, 7, 5]

    start_time = time.time()

    
    result = callQuickSortMulti(arr, 4)
    print(f"Time multi processes: {time.time() - start_time}")
    print(result)

    start_time = time.time()
    print(quicksort(arr))
    print(f"Time mono process: {time.time() - start_time}")