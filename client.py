import socket, _thread, hashlib, pyautogui, os

host = input("(Default: localhost) Server ip/domain: ")
if host == "": host = socket.gethostname()

port = input("(Default: 50505) Port: ")
if port == "": port = 50505
else: port = int(port)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))

password = s.recv(2048).decode()
if password == "pass":
    s.send(input("Server password: ").encode())
    if s.recv(2048).decode() == "no":
        print("Wrong password")
        exit()

username = input("Username: ")

s.send(username.encode())

def receive():
    global s

    while True:
        data = s.recv(1024).decode()
        if not data:
            os._exit(0)
            break
        print(data)

_thread.start_new_thread(receive,())

while True:
    message = pyautogui.prompt("Message")
    s.send(message.encode())
