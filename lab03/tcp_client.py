import socket
import threading
import sys

HOST = "127.0.0.1"
PORT = 65432
FILENAME = "html_files/folder1/a.txt"

#HOST = int(sys.argv[1])
#PORT = int(sys.argv[2])
#FILENAME = sys.argv[3]

request = f"GET /{FILENAME} HTTP/1.1\n\n"


def send_request():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))

    th_id = threading.get_ident()
    print(f"Threading id: {th_id}")

    client_socket.sendall(request.encode('utf-8'))

    data = client_socket.recv(1024)
    print(f"{th_id}: Sending data: {data}")
    client_socket.close()


##def test_send_many_requests():
##    for i in range(10):
##        send_request()


def main():
    print("Client started.")
    send_request()
##    for i in range(8):
##        client_thread = threading.Thread(target=test_send_many_requests, args=())
##        client_thread.start()


if __name__ == "__main__":
    main()
         
        
