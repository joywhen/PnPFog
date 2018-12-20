import socket


def send_data_with_broadcast(to_port, data):
    send_data('<broadcast>', to_port, data)


def send_data(to_address, to_port, data):
    is_broadcast = to_address == '<broadcast>'
    udp_socket = create_udp_socket(is_broadcast)
    udp_socket.sendto(data, (to_address, to_port))
    print(data.decode("utf-8"))


def create_udp_socket(is_broadcast):
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    if is_broadcast is True:
        udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    return udp_socket


if __name__ == '__main__':
    hello = "HELLO#,#NODE\n"
    send_data_with_broadcast(20001, hello.encode("utf-8"))
