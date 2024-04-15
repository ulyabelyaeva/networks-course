import random
import struct
import socket
from checksum import get_checksum

DEFAULT_PORT = 55555
DEFAULT_TIMEOUT = 0.1
DEFAULT_PACKET_SIZE = 1024


class Client:
    def __init__(self, port = DEFAULT_PORT, timeout = DEFAULT_TIMEOUT, \
                 psz = DEFAULT_PACKET_SIZE):
        self.server = '127.0.0.1'
        self.port = port
        self.timeout = timeout
        self.psz = psz


    def connect(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        except:
            return False
        self.socket.settimeout(self.timeout)
        return True


    def send_pkt(self, i: int, pkt: bytes) -> bool:
        addr = self.server, self.port
        for n_try in range(10):
            pkt[12:13] = struct.pack('b', n_try)

            ## imitate lost packets
            if random.randint(0, 100) > 29:
                self.socket.sendto(pkt, addr)

            try:
                data, _ = self.socket.recvfrom(self.psz)
                if data[8:11] == b'ASK':
                    return True
            except socket.timeout:
                print('\tTimeout for packet %d try %d' % (i, n_try))
                pass

        return False


    def send_data(self, buf: bytes):
        if self.connect():
            total = len(buf)
            pkt = bytearray(self.psz)
            sz = self.psz - 13
            n = total // sz
            if total % sz:
                n += 1
            print('Number of packets: %d' % n)

            pkt[:4] = struct.pack('i', 0)
            pkt[4:8] = struct.pack('i', total)
            pkt[8:12] = struct.pack('i', n)
            if not self.send_pkt(0, pkt):
                return False

            for i in range(n):
                i1, i2 = i * sz, min((i + 1) * sz, total)
                check = get_checksum(buf[i1:i2])
                pkt[:4] = struct.pack('i', i + 1)
                pkt[4:6] = struct.pack('H', check)
                pkt[13:] = buf[i1:i2]
                if self.send_pkt(i + 1, pkt):
                    print('Send packet %d check %d' % ((i + 1), check))
                    pass
                else:
                    print('Error sending packet # %d.' % (i + 1))
                    return False
            return True
        return False


def make_test_file(fn: str):
    test_data = ''.join(map(str, range(10000))).encode()
    f = open(fn, 'wb')
    f.write(test_data)
    f.close()


def read_file(fn: str) -> bytes:
    f = open(fn, 'br')
    res = f.read()
    f.close()
    return res


def check_files(f1, f2):
    return read_file(f1) == read_file(f2)

def main():
    fn = 'send.bin'
    # make_test_file(fn)
    client = Client()
    if client.send_data(read_file(fn)):
        print('Data was sent successfully.')

        if check_files(fn, 'received.bin'):
            print('Sent and received files are the same.')
        else:
            print('Sent and received files are different.')

if __name__ == '__main__':
    main()
