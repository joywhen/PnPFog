import socket
import threading
import APIHandler


def send_back(udp_data, udp_address):
    api_data_all = str(udp_data.decode("utf-8"))
    api_data_list = api_data_all[0:(len(api_data_all) - 1)].split("#,#")
    api_name = ''
    api_data = ''
    udp_ip_address = udp_address[0]
    udp_port = udp_address[1]
    try:
        api_name = api_data_list[0]
        api_data = api_data_list[1]
    finally:
        print("name:" + api_name)
        print("data:" + api_data)
        print("port:" + str(udp_port))
        print("ip:" + udp_ip_address)
    if api_name == "HELLO":  # to hello
        print("to hello handle")
        APIHandler.hello(api_data, udp_port, udp_ip_address)
    elif api_name == "NT":  # new task
        print("to new task handle")
        APIHandler.new_task(api_data, udp_port, udp_ip_address)
    elif api_name == "S":
        print("to S")
        APIHandler.get_s(api_data, udp_port, udp_ip_address)

    elif api_name == "QQQQQ":
        print("aaaaaaaa")


buffer_size = 1024
udp_socket_host = ''  # listen all ip
udp_socket_port = 20001  # port
udp_socket_address = (udp_socket_host, udp_socket_port)
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_socket.setblocking(1)
udp_socket.bind(udp_socket_address)
while True:
    udp_data, udp_address = udp_socket.recvfrom(buffer_size)
    thread = threading.Thread(target=send_back, args=(udp_data, udp_address))
    thread.start()


udp_socket.close()
