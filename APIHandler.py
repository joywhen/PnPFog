import UDPSender
import socket
import socket_echo_client_tcp
import FileUtil
import os
import json


device_udp_socket_port = 21001

work_dir = socket_echo_client_tcp.WORKDIR


class SJSONObject(json.JSONEncoder):
    def __jsonencode__(self):
        return {'type': self.type_, 'name': self.name, 'status': self.status}

    type_ = ""
    name = ""
    status = 0


class AdvancedJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, '__jsonencode__'):
            return obj.__jsonencode__()
        if isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)


def get_status_from_file(full_path):
    status = 0
    status_path = full_path + "/status.txt"
    print(status_path)
    if os.path.isfile(status_path) is True:
        file_context = open(status_path).readline()
        status = int(file_context)
    return status


def common_return_for_file(req_api, ip):
    count, object_list = get_task_count_and_task_obj_list(req_api, ip)
    json_list = json.dumps(object_list, cls=AdvancedJSONEncoder)
    final_str = req_api + str(json_list) + "\n"
    UDPSender.send_data(ip, device_udp_socket_port, bytes(final_str, 'utf-8'))

def get_task_count_and_task_obj_list(req_api, ip):
    now_path = "./" + work_dir + "/"
    FileUtil.check_path_and_createfolder(now_path)
    now_dir = os.listdir(now_path)
    object_list = []
    for dir_name in now_dir:
        full_dir_name = now_path + dir_name
        FileUtil.check_path_and_createfolder(full_dir_name)
        new_obj = SJSONObject()
        new_obj.type_ = "video"  # 写死
        new_obj.name = dir_name
        new_obj.status = get_status_from_file(full_dir_name)
        object_list.append(new_obj)
    count = len(object_list)
    return count, object_list



def get_s(data, port, ip):
    common_return_for_file("S#,#", ip)


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

    #
    ok_str = "NT#,#" + "OK" + "\n"
    # 然后返回OK
    UDPSender.send_data(ip, device_udp_socket_port, bytes(ok_str, 'utf-8'))


def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()

    return ip


def hello(data, port, ip):
    print(data) # 唯一编号
    if str(data).startswith("NODE"):
        # 查找是不是自己给自己发送的
        my_ip = get_host_ip()
        if my_ip != ip:
            # 不是给自己发送的
            count, object_list = get_task_count_and_task_obj_list("HELLO#,#", ip)



        print("ip:"+ip +"self:" + my_ip)

        # 自己节点上有的任务
        print("self")
    else:
        print("not self")
        # 要去查一下所有节点有没有在跑的任务

        common_return_for_file("HELLO#,#", ip)

