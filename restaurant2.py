import multiprocessing as mp
import random
import time
import curses

# Constants
NUM_SERVERS = 5
BUFFER_SIZE = 50
MIN_ORDER_INTERVAL = 3
MAX_ORDER_INTERVAL = 10
MIN_PREP_TIME = 2
MAX_PREP_TIME = 6
MENU_ITEMS = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')


def client_process(orders):
    """Simulates random orders from clients"""
    while True:
        order = (random.randint(1, 100), random.choice(MENU_ITEMS))
        orders.put(order)
        time.sleep(random.randint(MIN_ORDER_INTERVAL, MAX_ORDER_INTERVAL))


def server_process(server_id, orders, screen_lock, screen):
    """Simulates server taking orders and delivering to customers"""
    while True:
        order = orders.get()
        with screen_lock:
            screen.addstr(f"Server {server_id} taking order {order}\n")
        prep_time = random.randint(MIN_PREP_TIME, MAX_PREP_TIME)
        time.sleep(prep_time)
        with screen_lock:
            screen.addstr(f"Server {server_id} delivering order {order}\n")


def display_process(orders, screen_lock, screen):
    """Displays the orders waiting to be fulfilled"""
    while True:
        with screen_lock:
            screen.addstr(f"Orders waiting: {list(orders.queue)}\n")
            screen.addstr(f"Number of orders waiting: {orders.qsize()}\n")
        time.sleep(1)


if __name__ == '__main__':
    # Shared resources
    orders = mp.Queue(BUFFER_SIZE)
    screen_lock = mp.Lock()

    # Initialize curses screen
    screen = curses.initscr()
    curses.noecho()
    curses.cbreak()

    # Create and start client process
    client = mp.Process(target=client_process, args=(orders,))
    client.start()

    # Create and start server processes
    servers = []
    for i in range(NUM_SERVERS):
        server = mp.Process(target=server_process, args=(i, orders, screen_lock, screen,))
        server.start()
        servers.append(server)

    # Start display process
    display = mp.Process(target=display_process, args=(orders, screen_lock, screen,))
    display.start()

    # Wait for processes to finish
    client.join()
    for server in servers:
        server.join()
    display.join()

    # Clean up curses screen
    curses.nocbreak()
    curses.echo()
    curses.endwin()
