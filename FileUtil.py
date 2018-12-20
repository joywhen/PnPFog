import os


def check_path_and_createfolder(path):
    if not os.path.exists(path):
        os.makedirs(path)
        print("mkdir success")
    else:
        print("There is the path")
