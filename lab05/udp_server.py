import socket
import datetime
from time import sleep

def main():
    interfaces = socket.getaddrinfo(host=socket.gethostname(), port=None, family=socket.AF_INET)
    allips = [ip[-1][0] for ip in interfaces]

    while True:
        msg = str(datetime.datetime.now())

        for ip in allips:
            print(f'sending on {ip}')
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)  # UDP
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            sock.bind((ip,0))
            sock.sendto(msg.encode(), ("255.255.255.255", 12000))
            sock.close()

        sleep(1)


main()
