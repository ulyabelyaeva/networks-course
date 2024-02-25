import socket
import threading
import sys
import time

HOST = "127.0.0.1"
PORT = 65432
concurrency_limit = 6

#PORT = int(sys.argv[1])
#concurrency_limit = int(sys.argv[2])

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)



def handle_client(client_socket):
    th_id = threading.get_ident()
    print(f"Threading id: {th_id}")

    data = client_socket.recv(1024)
    if not data:
        return
    print(f"{th_id}: Got request data: {data}")

    path = data.split()[1][1:]

    try:
        with open(path, 'r') as f:
            content = f.read()
            header = 'HTTP/1.1 200 OK\n\n'.encode('utf-8')
            response = ('<html><body>' + content + '</body></html>').encode('utf-8')
        print("{th_id}: Sending 200 OK")
    except:
        header = 'HTTP/1.1 404 Not Found\n\n'.encode('utf-8')
        response = ('<html><body>' + 'No such file on server' + '</body></html>').encode('utf-8')
        print("{th_id}: Sending 404 Not Found")

    client_socket.sendall(header + response)
    client_socket.close()


def main():
    print("Server started. Waiting for connections...")

    while True:
        while threading.activeCount() >= concurrency_limit:
            time.sleep(0.002)
        client_socket, client_address = server_socket.accept()
        print(f"Connected to {client_address}")
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()


if __name__ == "__main__":
    main()
         
        
