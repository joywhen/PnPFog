import socket
import UDPSender
import json


device_udp_socket_port = 21001


def new_task(data, port, ip):
    params = str(data).split(",")
    uuid = ""
    type_ = ""
    url = ""
    if len(params) == 3:
        uuid = params[0]
        type_ = params[1]
        url = params[2]
    print(uuid)
    print(type_)
    print(url)
    # 提交给服务器

    # 然后返回OK
    


def hello(data, port, ip):
    print(data) # 唯一编号
    # 要去查一下所有节点有没有在跑的任务
    task_list = []


    task_list_json_str = json.dumps(task_list)
    return_str = "HELLO#,#" + task_list_json_str + "\n"  # return str
    UDPSender.send_data(ip, device_udp_socket_port, bytes(return_str, 'utf-8'))

