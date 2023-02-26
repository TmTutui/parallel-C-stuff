import multiprocessing
import curses
import random
import time

from MultiQueue import MyQueue


# Constants
NUM_SERVEURS = 5
WAIT_TIME_MIN = 3
WAIT_TIME_MAX = 10
MAX_COMMANDS = 50
MENUS = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')


def client(command_queue):
    while True:
        time.sleep(random.randint(1, 2))
        identifiant = random.randint(1, 1000)
        menu = random.choice(MENUS)
        command = (identifiant, menu)
        command_queue.put(command)


def serveur(serveur_id, command_queue):
    while True:
        if not command_queue.empty():
            command = command_queue.get()
            print(f"Le serveur {serveur_id} traite la commande {command}")
            time.sleep(random.randint(WAIT_TIME_MIN, WAIT_TIME_MAX))
            print(f"La commande {command} est prête")
        else:
            time.sleep(1)


def major_dHomme(command_queue):
    screen = curses.initscr()
    curses.curs_set(0)
    timestamp = 0

    screen.addstr(0, 0, f"Time: {timestamp}")
    screen.addstr(1, 0, "Commandes clients en attente: []")
    screen.addstr(2, 0, f"Nombre de commandes en attente: {command_queue.qsize()}")
    screen.refresh()

    while True:
        timestamp+=1
        screen.addstr(0, 0, f"Time: {timestamp}")
        screen.addstr(1, 0, "Commandes clients en attente: " + str(command_queue.elements()))
        screen.addstr(2, 0, f"Nombre de commandes en attente: {command_queue.qsize()}")
        screen.refresh()
        time.sleep(1)


if __name__ == '__main__':
    command_queue = MyQueue()
    # command_queue = multiprocessing.Queue()

    client_process = multiprocessing.Process(target=client, args=(command_queue,))
    serveur_processes = [multiprocessing.Process(target=serveur, args=(i, command_queue,)) for i in range(1, NUM_SERVEURS+1)]
    major_dHomme_process = multiprocessing.Process(target=major_dHomme, args=(command_queue,))

    client_process.start()
    for process in serveur_processes:
        process.start()
    major_dHomme_process.start()

    client_process.join()
    for process in serveur_processes:
        process.join()
    major_dHomme_process.join()

    curses.endwin()

