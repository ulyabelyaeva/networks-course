import socket
import threading
import sys

HOST = "127.0.0.1"
PORT = 65432


def send_request():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))

    message = input(" -> ")

    while message.lower().strip() != 'bye':
        client_socket.send(message.encode())
        data = client_socket.recv(1024).decode()

        print('Received from server: ' + data)

        message = input(" -> ")

    client_socket.close()


def main():
    print("Client started.")
    send_request()


if __name__ == "__main__":
    main()
         
        
