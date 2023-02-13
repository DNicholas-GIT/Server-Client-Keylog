import socket
import threading
import os
from csv import writer

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE= "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

master_csv = "master_log.csv"

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected")

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False

            print(f"{msg}")
            Append_master_csv(msg)



    conn.close()


def Append_master_csv(msg):
    if os.path.isfile(master_csv)==False:
        with open(master_csv, 'a') as write_obj:
            msg_starter = msg[:-2]
            msg_end = msg_starter[2:]
            write_obj.write(msg_end)
    else:
        with open(master_csv, 'a') as write_obj:
            # msg_adder = msg[:-1]
            msg_done = msg[2:]
            new_text = msg_done.split(",")
            new_text = new_text[:-1]
            writer_object = writer(write_obj)
            writer_object.writerow(new_text)

            

def start_server():
    server.listen()
    print(f"Server is now [LISTENING]")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")




def manager():
    print(f"[STARTING SERVER] PORT: {PORT} IP: {SERVER}")
    start_server()


manager()