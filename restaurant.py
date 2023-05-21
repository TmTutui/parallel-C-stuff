import multiprocessing as mp
import random
import time
import curses


def client_process(command_queue):
    while True:
        # Generate a random command
        client_id = random.randint(1, 100)
        menu = chr(random.randint(ord('A'), ord('Z')))
        command = (client_id, menu)
        print(f"New command: {command}")
        
        # Put the command in the command queue
        command_queue.put(command)
        
        # Wait for a random amount of time before generating another command
        time.sleep(random.randint(1, 2))


def server_process(server_id, command_queue, cooked_queue):
    while True:
        # Get the next command from the command queue
        command = command_queue.get()
        print(f"Server {server_id} processing command {command}")
        
        # Simulate cooking time
        time.sleep(random.randint(1, 5))
        
        # Put the cooked command in the cooked queue
        cooked_queue.put((server_id, command))


def delivery_process(cooked_queue):
    while True:
        # Get the next cooked command from the cooked queue
        server_id, command = cooked_queue.get()
        print(f"Command {command} delivered by server {server_id}")
        

def display_process():
    """Displays the orders waiting to be fulfilled"""
    while True:
        with screen_lock:
            screen.addstr(f"Orders waiting: {list(orders.queue)}\n")
            screen.addstr(f"Number of orders waiting: {orders.qsize()}\n")
        time.sleep(1)


if __name__ == '__main__':
    # Create the command queue and cooked queue
    command_queue = mp.Queue(50)
    cooked_queue = mp.Queue(50)

    screen_lock = mp.Lock()

    # Initialize curses screen
    screen = curses.initscr()
    curses.noecho()
    curses.cbreak()

    # Start the client process
    client = mp.Process(target=client_process, args=(command_queue, ))
    client.start()
    
    # Start the server processes
    num_servers = 5
    servers = []
    for i in range(num_servers):
        server = mp.Process(target=server_process, args=(i+1, command_queue, cooked_queue))
        server.start()
        servers.append(server)
    
    # Start the delivery process
    delivery = mp.Process(target=delivery_process, args=(cooked_queue,))
    delivery.start()
    
    # Wait for all processes to finish
    client.join()
    for server in servers:
        server.join()
    delivery.join()
