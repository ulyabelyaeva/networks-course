import time
import socket
import struct
import select
import random
import asyncore

ICMP_ECHO_REQUEST = 8
ICMP_CODE = socket.getprotobyname('icmp')


def checksum(source_string):
    sum = 0
    count_to = (len(source_string) / 2) * 2
    count = 0
    while count < count_to:
        this_val = source_string[count + 1]*256+source_string[count]
        sum = sum + this_val
        sum = sum & 0xffffffff
        count = count + 2
    if count_to < len(source_string):
        sum = sum + ord(source_string[len(source_string) - 1])
        sum = sum & 0xffffffff
    sum = (sum >> 16) + (sum & 0xffff)
    sum = sum + (sum >> 16)
    answer = ~sum
    answer = answer & 0xffff
    answer = answer >> 8 | (answer << 8 & 0xff00)
    return answer


def create_packet(id):
    header = struct.pack('bbHHh', ICMP_ECHO_REQUEST, 0, 0, id, 1)
    data = 192 * 'Q'
    my_checksum = checksum(header + data.encode())
    header = struct.pack('bbHHh', ICMP_ECHO_REQUEST, 0,
                         socket.htons(my_checksum), id, 1)
    return header + data.encode()


def do_one(dest_addr, timeout=1):
    with socket.socket(socket.AF_INET, socket.SOCK_RAW, ICMP_CODE) as my_socket:
        host = socket.gethostbyname(dest_addr)
        packet_id = int((id(timeout) * random.random()) % 65535)
        packet = create_packet(packet_id)
        while packet:
            sent = my_socket.sendto(packet, (dest_addr, 1))
            packet = packet[sent:]
        delay = receive_ping(my_socket, packet_id, time.time(), timeout)
    return delay


def receive_ping(my_socket, packet_id, time_sent, timeout):
    time_left = timeout
    while True:
        started_select = time.time()
        ready = select.select([my_socket], [], [], time_left)
        how_long_in_select = time.time() - started_select
        if ready[0] == []: # Timeout
            return
        time_received = time.time()
        rec_packet, addr = my_socket.recvfrom(1024)
        icmp_header = rec_packet[20:28]
        type, code, checksum, p_id, sequence = struct.unpack(
            'bbHHh', icmp_header)
        if p_id == packet_id:
            return time_received - time_sent
        time_left -= time_received - time_sent
        if time_left <= 0:
            return


def verbose_ping(dest_addr, timeout=2, count=4):
    delays = []
    sent = received = 0
    print('Pinging {}...'.format(dest_addr))
    for i in range(count):
        delay = do_one(dest_addr, timeout)
        sent += 1
        if delay == None:
            print('No reply from {} (Timeout within {} seconds.)'.format(dest_addr, timeout))
        else:
            received += 1
            delay = round(delay * 1000.0)
            print('Reply from {}: time={}ms'.format(dest_addr, delay))
            delays.append(delay)
        time.sleep(1)
    if len(delays) == 0:
        return
    info = '''Ping statistics for {dest_addr}:
    Packets: Sent = {sent}, Received = {received}, Lost = {lost} ({loss}% loss),
Approximate round trip times in milli-seconds:
    Minimum = {min_}ms, Maximum = {max_}ms, Average = {avg}ms'''.format(
        dest_addr=dest_addr,
        sent=sent,
        received=received,
        lost=sent - received,
        loss=(sent - received) / sent * 100,
        min_=min(delays),
        max_=max(delays),
        avg=round(sum(delays) / len(delays))
    )
    print()
    print(info)
    print()


##verbose_ping('google.com')
##verbose_ping('srdhfgjhkukgjffdxgxfhgj.com')
##verbose_ping('127.0.0.1')
##verbose_ping('192.168.0.1')
verbose_ping('ya.ru')
verbose_ping('daat.com')
verbose_ping('daat.com', timeout=0.116)
