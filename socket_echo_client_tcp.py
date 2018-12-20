#!/usr/bin/python
import sys
import os
import socket
import struct
import requests
import time
import subprocess
import FileUtil

TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 1024
WORKDIR = 'work'


def download_from_server(url):
    print("Downloading with request")
    # print(time.time())
    r = requests.get(url)
    with open("./test4.mp3", "wb") as code:
        print("Downloading...")
        code.write(r.content)
    # print(time.time())
    print("Download over")

    # get time(ms) and create folder
    nowTime = int(round(time.time() * 1000))
    nowPath = "./" + WORKDIR + "/" + str(nowTime)
    FileUtil.check_path_and_createfolder(nowPath)
    FileUtil.check_path_and_createfolder(nowPath + "/output")
    nowStatusPath = nowPath + "/status.txt"
    # check_path_and_createfolder(nowStatusPath)

    print("Clip start...")
    with open(nowStatusPath, 'w') as fp:
        fp.write("1")

    type = 'audio'
    if type == 'video':
        start = 0
        filename = 'test3.avi'
        video_time = 227
        num = 0
        videoPath = nowPath + "/output/video"
        while start <= video_time - 5:
            print(subprocess.Popen("ffmpeg -ss " + str(start) + " -i " + str(filename) + " -t 5 " + videoPath + str(num) + ".mp4",
                                   shell=True).wait())
            start = start + 5
            num = num + 1

        print(subprocess.Popen("ffmpeg -ss " + str(start) + " -i " + str(filename) + " -t " + str(video_time - start) + " " + videoPath + str(num) + ".mp4",
                               shell=True).wait())
    elif type == 'audio':
        start = 0
        filename = 'test4.mp3'
        audio_time = 215
        num = 0
        audioPath = nowPath + "/output/audio"
        while start <= audio_time - 20:
            print(subprocess.Popen(
                "ffmpeg -ss " + str(start) + " -i " + str(filename) + " -t 20 " + audioPath + str(num) + ".aac",
                shell=True).wait())
            start = start + 20
            num = num + 1

        print(subprocess.Popen("ffmpeg -ss " + str(start) + " -i " + str(filename) + " -t " + str(
            audio_time - start) + " " + audioPath + str(num) + ".aac", shell=True).wait())
    else:
        filename = 'test5.jpg'
        imagePath = nowPath + "/output/image.png"
        print(subprocess.Popen("ffmpeg -i " + filename + " " + imagePath, shell=True).wait())
    print("Clip end...")

    return nowPath


def socket_client(nowPath):
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
        # path = './output/'
        path = nowPath + "/output/"
        FileUtil.check_path_and_createfolder(path)
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
            fp_temp.write("file " + path + file_temp + "\n")
        fp_temp.close()

        with open(nowPath + "/status.txt", 'w') as fp:
            fp.write("2")

        for filepath in filepatharr:
            if os.path.isfile("" + path + filepath):
                fileinfo_size = struct.calcsize('128sl')
                # print(os.path.basename(filepath))
                fhead = struct.pack(
                    '128sl',
                    bytes(os.path.basename(filepath), 'utf-8'),
                    os.stat("" + path + filepath).st_size
                )
                # print(fhead)
                s.send(fhead)
                print("client filepath:{}".format(filepath))

                fp = open("" + path + filepath, 'rb')
                while True:
                    data = fp.read(BUFFER_SIZE)
                    if not data:
                        print("file send over")

                        with open(nowPath + "/status.txt", 'w') as fp:
                            fp.write("3")
                        break
                    s.send(data)
                fp.close()

        # TODO Solve error
        s.close()
        break




if __name__ == '__main__':
    nowPath = download_from_server("http://192.168.2.100/audio.mp3")
    socket_client(nowPath)