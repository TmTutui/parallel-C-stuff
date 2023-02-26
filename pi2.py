import math
from multiprocessing import Process, Queue
import time
from decimal import Decimal

def gauss_legendre(num_iterations, output):
    # Initialize variables
    a = Decimal(1.0)
    b = Decimal(1.0) / Decimal(2).sqrt()
    t = Decimal(1.0) / Decimal(4.0)
    p = Decimal(1.0)

    # Iterate
    for i in range(num_iterations):
        a_new = (a + b) / Decimal(2.0)
        b = (a * b).sqrt()
        t -= p * (a - a_new) ** Decimal(2)
        p *= Decimal(2.0)
        a = a_new

    # Calculate pi estimate
    pi_estimate = ((a + b) ** Decimal(2)) / (Decimal(4.0) * t)
    output.put(pi_estimate)


if __name__ == '__main__':
    num_iterations = 1000000
    num_processes = 4

    output = Queue()

    processes = [Process(target=gauss_legendre, args=(num_iterations // num_processes, output)) for _ in range(num_processes)]

    time_start = time.time()
    for p in processes:
        p.start()

    for p in processes:
        p.join()

    print(output)

    pi_estimate = sum(output.get() for _ in range(num_processes)) / num_processes
    print(f"Time 4 processes: {time.time() - time_start}")

    time_start = time.time()
    gauss_legendre(num_iterations, output)
    print(f"Time 1 process: {time.time() - time_start}")

    print(f"Estimated value of pi: {pi_estimate}")