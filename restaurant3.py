import multiprocessing
import curses
import random
import time

from MultiQueue import MyQueue


# Constants
NUM_SERVEURS = 5
WAIT_TIME_MIN = 5
WAIT_TIME_MAX = 10
MAX_COMMANDS = 50
MENUS = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')


def replaceQueue(serveur_queue, serveur_id, new_command):
    for i in range(serveur_queue.qsize()):
        curr_id, command = serveur_queue.get()
        
        if(curr_id == serveur_id):
            serveur_queue.put((curr_id, new_command))
            break

        serveur_queue.put((curr_id, command))


def client(command_queue):
    while True:
        time.sleep(random.randint(1, 2))
        identifiant = random.randint(1, 1000)
        menu = random.choice(MENUS)
        command = (identifiant, menu)
        command_queue.put(command)


def serveur(serveur_id, command_queue, serveur_queue):
    while True:
        if not command_queue.empty():
            command = command_queue.get()

            replaceQueue(serveur_queue, serveur_id, command)

            time.sleep(random.randint(WAIT_TIME_MIN, WAIT_TIME_MAX))
            
            replaceQueue(serveur_queue, serveur_id, None)

        else:
            time.sleep(1)


def display_serveurs(serveur_queue, screen):
    serveurs = serveur_queue.get_all()
    
    for serveur_id, command in serveurs:
        if(command):
            screen.addstr(serveur_id, 0, f"Le serveur {serveur_id} traite la commande {command} ")
        else:
            screen.addstr(serveur_id, 0, f"Le serveur {serveur_id} traite rien")


def major_dHomme(command_queue, serveur_queue):
    screen = curses.initscr()
    curses.curs_set(0)
    timestamp = 0

    while True:
        timestamp+=1

        screen.addstr(0, 0, f"Time: {timestamp}")
        display_serveurs(serveur_queue, screen)

        screen.addstr(1+NUM_SERVEURS, 0, "Commandes clients en attente: " + str(command_queue.get_all()))
        screen.addstr(2+NUM_SERVEURS, 0, f"Nombre de commandes en attente: {command_queue.qsize()}\n\n")
        
        screen.refresh()
        time.sleep(1)
        screen.erase()


if __name__ == '__main__':
    command_queue = MyQueue(maxsize=10)
    serveur_queue = MyQueue(maxsize=NUM_SERVEURS)
    # command_queue = multiprocessing.Queue()

    client_process = multiprocessing.Process(target=client, args=(command_queue,))
    
    serveur_processes = []
    for i in range(1, NUM_SERVEURS+1):
        serveur_processes.append(multiprocessing.Process(target=serveur, args=(i, command_queue, serveur_queue,)))
        serveur_queue.put((i, None))
    
    major_dHomme_process = multiprocessing.Process(target=major_dHomme, args=(command_queue, serveur_queue,))

    client_process.start()
    for process in serveur_processes:
        process.start()
    major_dHomme_process.start()

    client_process.join()
    for process in serveur_processes:
        process.join()
    major_dHomme_process.join()

    curses.endwin()

