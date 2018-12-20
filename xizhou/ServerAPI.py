# run in the server
import socket
import threading
import os
import json

tcp_listen_port = 30000
max_connection = 10


def main():
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    local_address = ('', tcp_listen_port)
    tcp_socket.bind(local_address)
    tcp_socket.listen(max_connection)
    try:
        while True:
            new_socket, destaddr = tcp_socket.accept()
            client = threading.Thread(target=send_back, args=(new_socket, destaddr))
            client.start()
    finally:
        tcp_socket.close()

def send_back(new_socket, destaddr):
    new_message = b''
    while True:
        new_a = new_socket.recv(1024)
        new_message += new_a
        if new_a.decode('utf-8').endswith('\n') is True:
            break
    print(new_message)
    new_socket.send(list_files().encode("utf-8"))
    new_socket.close()


def list_files():
    list = os.listdir("/home/zhouxi/")
    return str(json.dumps(list))


if __name__ == '__main__':
    main()
