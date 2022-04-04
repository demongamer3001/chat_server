import socket, hashlib, json
from _thread import *

cfg = json.load( open("settings.json", "r") )["server"]

client_count = 32
port = cfg["port"]
username_blacklist = "server admin moderator".split(" ")
password = "" # Leave empty for no password


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
ThreadCount = 0

s.bind((host, port))

print(f"Chat server started on port {port}.")

s.listen(client_count)

clients = {}

def send_all(text, exclude = []): # Send a message to all clients
    for c in clients.keys():
        if c in exclude:
            continue
        c.send(str(text).encode())


def threaded_client(connection):
    global ThreadCount, clients

    connection.send("[SERVER] Hello!".encode()) # Send message to new client
    while True:
        try:
            data = connection.recv(2048).decode()
        except:
            break
        for c in clients.keys():
            if c is connection:
                continue
            try:
                c.send(f'[{clients[connection]}] {data}'.encode())
            except:
                break
    username = clients.pop(connection)
    ThreadCount -= 1

    print(f"W: {username} left")

    print(f"Thread amount: {ThreadCount}/{client_count}")

    send_all(f"{username} just left!")
    print()
    connection.close()

while True:
    conn, address = s.accept()

    if password != "":
        conn.send("pass".encode())
        tmp = conn.recv(2048).decode() # Password
        if tmp != password:
            conn.send("no".encode())
            conn.close()
            continue
        else: 
            conn.send("yes".encode())
    else:
        conn.send("nopass".encode())

    tmp = conn.recv(2048).decode() # Username
    if tmp.lower() in username_blacklist or tmp in clients.values():
        if tmp.lower() in username_blacklist:
            conn.send("E: This username is on the blacklist.".encode())
        elif tmp in clients.values():
            conn.send("E: This username is already in use.".encode())
        
        conn.close()
        continue

    clients[conn] = tmp

    send_all(f"{tmp} just joined!",exclude = [conn])

    print(f"N: {tmp} joined ({address[0]})")
    start_new_thread(threaded_client, (conn, ))
    ThreadCount += 1
    print(f"Thread amount: {ThreadCount}/{client_count}")
ServerSocket.close()
