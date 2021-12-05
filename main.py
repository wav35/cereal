# Serial and sequential floating text across multiple clients!
# Use case: Demonstrate connecting multiple clients in the network
from time import sleep
from os import get_terminal_size, name, system
from figlets import letters
from utilities import transform_figlets, print_figlet_array, get_local_ip
from server import CerealServer
from client import CerealClient

(cols, rows) = get_terminal_size()
clear_func = "cls" if name == "nt" else "clear"

for fig in letters:
    letters[fig] = transform_figlets(letters[fig])

print("Welcome to Cereal!")
command = input("(h)ost a cereal or (j)oin an existing cereal:    ").lower()

if command == "h":
    nclients = int(input("How many clients do you want?    "))
    srv = CerealServer()
    _, port = srv.start_server()
    local_ip = get_local_ip()
    
    cur_nclients = -1

    while True:
        sleep(0.5)
        len_clients = len(srv.clients)
        if len_clients != cur_nclients:
            system(clear_func)
            print("Server created! Please share this address: %s:%d" % (local_ip, port))
            print("Clients connected: %d" % (len_clients))
            cur_nclients = len_clients
            for i, client in enumerate(srv.clients):
                print(i, client["width"])

        if len_clients == nclients:
            break

    sentence = input("Enough clients joined! Please enter your sentence:   ").lower()
    srv.send_content(sentence)
    input("Content sent to clients. Please press ENTER for magic...\n> ")
    srv.display_marquee()
    sleep(9999) # The function sometimes exits before all socket payloads are sent!
elif command == "j":
    addr = input("Please enter the address:\n> ")
    client = CerealClient(cols)
    parts = addr.split(":")
    (fig_array, rel_offset) = client.connect_to_addr(parts[0], int(parts[1]))

    figlet_offset = 0
    while True:
        print_figlet_array(fig_array, figlet_offset, figlet_offset+cols)
        figlet_offset += 1
        sleep(0.1)
        system(clear_func)

