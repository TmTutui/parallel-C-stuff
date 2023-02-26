import random
import multiprocessing
import time

def approx_pi(num_samples):
    count = 0
    for i in range(num_samples):
        x = random.random()
        y = random.random()
        if x**2 + y**2 <= 1:
            count += 1

    return 4 * count / num_samples


if __name__ == '__main__':
    num_samples = 1000000
    num_processes = 4
    pool = multiprocessing.Pool(num_processes)
    
    time_start = time.time()
    results = pool.map(approx_pi, [num_samples // num_processes] * num_processes)
    pi_approx = sum(results) / num_processes
    print(f"Time 4 processes: {time.time() - time_start}")

    time_start = time.time()
    results = approx_pi(num_samples)
    print(f"Time 1 process: {time.time() - time_start}")

    print('Approximation de Pi: {}'.format(pi_approx))