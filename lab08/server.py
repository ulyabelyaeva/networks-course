import sys
import random
import socket
import struct
from checksum import check_checksum

DEFAULT_PORT = 55555
DEFAULT_PACKET_SIZE = 1024


class Server:
    def __init__(self, port, psz):
        self.port = port
        self.psz = psz
        self.data = {}

    def start(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(('', self.port))

        while True:
            buf, addr = self.socket.recvfrom(self.psz)
            np = struct.unpack('i', buf[:4])[0]
            if np == 0:
                total = struct.unpack('i', buf[4:8])[0]
                num = struct.unpack('i', buf[8:12])[0]
                self.data[addr] = num, bytearray(total)
                check = 0
            else:
                check = struct.unpack('H', buf[4:6])[0]
            nt = struct.unpack('b', buf[12:13])[0]
            print('Packet # %d was received, try is %d, check is %d' % (np, nt, check))

            ## imitate lost packets
            if random.randint(0, 100) < 30:
                print('Imitate lost for packet %d try %d' % (np, nt))
                continue

            if np == 0:
                is_check = True
            else:
                is_check = check_checksum(buf[13:], check)
            resp = bytearray(12)
            resp[:8] = buf[:8]
            if is_check:
                resp[8:] = b'ASK '
            else:
                resp[8:] = b'RETR'
            self.socket.sendto(resp, addr)

            if np > 0:
                total = len(self.data[addr][1])
                sz = self.psz - 13
                i1 = (np - 1) * sz
                i2 = min(total, np * sz)
                self.data[addr][1][i1:i2] = buf[13:13 + i2 - i1]
                if np == self.data[addr][0]:
                    self.save_file('received.bin', addr)
                    del self.data[addr]


    def save_file(self, fn, addr):
        f = open(fn, 'wb')
        f.write(self.data[addr][1])
        f.close()

def get_args():
    port, psz = DEFAULT_PORT, DEFAULT_PACKET_SIZE
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except:
            pass
    if len(sys.argv) > 2:
        try:
            psz = int(sys.argv[2])
        except:
            pass
    return port, psz


def main():
    port, psz = get_args()
    server = Server(port, psz)
    server.start()


if __name__ == '__main__':
    main()
