#!/usr/bin/python
import socket
import threading
import time
import sys
import os
import struct

TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 1024

# create a tcp socket
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.bind((TCP_IP, TCP_PORT))
# s.listen(1)


def socket_service():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((TCP_IP, TCP_PORT))
        s.listen(10)
    except socket.error as e:
        print(e)
        sys.exit(1)
    print("Waiting connection...")

    while True:
        conn, addr = s.accept()
        t = threading.Thread(
            target=deal_data, args=(conn, addr)
        )
        t.start()


def deal_data(conn, addr):
    print("Accept new connection from {0}".format(addr))
    conn.send("Welcome to the server".encode('utf-8'))

    while True:
        fileinfo_size = struct.calcsize('128sl')
        buf = conn.recv(fileinfo_size)
        if buf:
            filename, filesize = struct.unpack('128sl', buf)
            filename = str(filename, 'utf-8')
            filename = filename.strip('\00')
            new_filename = os.path.join('./input/', filename)
            print("new filename is {0}, filesize is {1}".format(new_filename, filesize))

            recv_size = 0
            fp = open(new_filename, 'wb')
            print("Start receving...")

            while not recv_size == filesize:
                if filesize - recv_size > BUFFER_SIZE:
                    data = conn.recv(BUFFER_SIZE)
                    recv_size += len(data)
                else:
                    data = conn.recv(filesize- recv_size)
                    recv_size = filesize
                fp.write(data)
            fp.close()
            print("End receive")

        # conn.close()
        # break
    # conn.close()


if __name__ == '__main__':
    socket_service()