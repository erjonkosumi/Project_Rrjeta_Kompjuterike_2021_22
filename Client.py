import socket
import threading

nickname = input("Choose Your Nickname:")
#Promt client te jep adresen IP, nese nuk ka specifike i tregohet default(serveri yne)
host=input("Jepni IP adresen lokale(default:127.0.0.1): ")
if nickname == 'admin':
    password = input("Enter Password for Admin:")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Qasja tek hosti
client.connect((host, 5555))

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
                # Klientet te cilat jane ne ban list, nuk kan mundesi qasje serish ne server.
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
# Getting Messages
        message = f'{nickname}: {input("")}'
        if message[len(nickname) + 2:].startswith('/'):
            if nickname == 'admin':
                if message[len(nickname) + 2:].startswith('/kick'):
                    # 2 per : dhe spacebar dhe 6 per komanden /KICK_
                    client.send(f'KICK {message[len(nickname) + 2 + 6:]}'.encode('ascii'))
                elif message[len(nickname) + 2:].startswith('/ban'):
                    # 2 per : dhe spacebar dhe 5 per komanden /BAN
                    client.send(f'BAN {message[len(nickname) + 2 + 5:]}'.encode('ascii'))
            else:
                print("Commands can be executed by Admins only !!")
        else:
            client.send(message.encode('ascii'))


recieve_thread = threading.Thread(target=receive)
recieve_thread.start()
write_thread = threading.Thread(target=write)
write_thread.start()
