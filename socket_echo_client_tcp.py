#!/usr/bin/python
import sys
import os
import socket
import struct

TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 1024
MESSAGE = b'HELLO, World'

def socket_client():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((TCP_IP, TCP_PORT))
    except socket.error as e:
        print(e)
        sys.exit(1)

    print(s.recv(BUFFER_SIZE))

    while True:
        # TODO filepath dynamic
        filepatharr = []
        path = './output/'
        dirs = os.listdir(path)
        for file in dirs:
            if os.path.splitext(file)[1] == '.aac':
                # new_file = os.path.join(path, file)
                # filepatharr.append(new_file)
                filepatharr.append(file)

        # TODO Sort filepatharr
        filepatharr.sort()
        filepatharr = sorted(filepatharr, key=lambda i:len(i),reverse=False)
        print(filepatharr)

        # TODO Write file name list to text file
        fp_temp = open("output.txt", 'w')
        for file_temp in filepatharr:
            fp_temp.write("file" + " ./output/" + file_temp + "\n")
        fp_temp.close()

        for filepath in filepatharr:
            if os.path.isfile('./output/' + filepath):
                fileinfo_size = struct.calcsize('128sl')
                # print(os.path.basename(filepath))
                fhead = struct.pack(
                    '128sl',
                    bytes(os.path.basename(filepath), 'utf-8'),
                    os.stat('./output/'+ filepath).st_size
                )
                # print(fhead)
                s.send(fhead)
                print("client filepath:{}".format(filepath))

                fp = open('./output/' + filepath, 'rb')
                while True:
                    data = fp.read(BUFFER_SIZE)
                    if not data:
                        print("file send over")
                        break
                    s.send(data)
                fp.close()

        # TODO Solve error
        s.close()
        break


if __name__ == '__main__':
    socket_client()