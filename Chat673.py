from socket import *
from threading import *

# Phones address or the LOCAL port in UDP application
phone_name = "172.23.23.162"
phone_port = 4000

# Macbook address or the remote port in UDP application
mac_name = '172.23.22.140'
mac_port = 13000

# We create socket that uses UDP and IPv4 and bind it to our phone's IP address

chatsocket = socket(AF_INET, SOCK_DGRAM)
chatsocket.bind(('', mac_port))

def receive_chat():
    while 1:
        message = chatsocket.recvfrom(2048)
        if message[0].decode().lower() == "quit":
            break
        else:
            print("\nReceived message from phone :", message[0].decode())


def send_chat():
    while 1:
        message = input("Enter your message: ")
        if message.lower() == "quit":
            break
        else:
            chatsocket.sendto(message.encode(), (phone_name, phone_port))


# Please enter quit on both phone and laptop to quit the code .
receive_thread = Thread(target=receive_chat)
send_thread = Thread(target=send_chat)

receive_thread.start()
send_thread.start()

receive_thread.join()
send_thread.join()


chatsocket.close()
