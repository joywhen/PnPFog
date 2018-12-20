import UDPSender
import json
import socket_echo_client_tcp
import FileUtil
import os


device_udp_socket_port = 21001

work_dir = socket_echo_client_tcp.WORKDIR


def get_s(data, port, ip):
    now_path = "./" + work_dir + "/"
    FileUtil.check_path_and_createfolder(now_path)
    now_dir = os.listdir(now_path)


    print(now_dir)


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
    # 提交给node

    # 然后返回OK
    


def hello(data, port, ip):
    print(data) # 唯一编号
    # 要去查一下所有节点有没有在跑的任务
    task_list = []


    task_list_json_str = json.dumps(task_list)
    return_str = "HELLO#,#" + task_list_json_str + "\n"  # return str
    UDPSender.send_data(ip, device_udp_socket_port, bytes(return_str, 'utf-8'))

