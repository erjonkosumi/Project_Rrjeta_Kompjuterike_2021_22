import socket
import threading

nickname = input("Choose Your Nickname:")
if nickname == 'admin':
    password = input("Enter Password for Admin:")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Connect to a host
client.connect(('127.0.0.1', 5555))

stop_thread = False


def receive():
    while True:
        global stop_thread
        if stop_thread:
            break
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                client.send(nickname.encode('ascii'))
                next_message = client.recv(1024).decode('ascii')
                if next_message == 'PASS':
                    client.send(password.encode('ascii'))
                    if client.recv(1024).decode('ascii') == 'REFUSE':
                        print("Connection is Refused !! Wrong Password")
                        stop_thread = True
                # Clients those are banned can't reconnect
                elif next_message == 'BAN':
                    print('Connection Refused due to Ban')
                    client.close()
                    stop_thread = True
            else:
                print(message)
        except:
            print('Error Occured while Connecting')
            client.close()
            break


def write():
    while True:
        if stop_thread:
            break
