import os
import shutil
from pathlib import Path
import os


class ProcessFile:

    def __init__(self):
        print(" I am inside init function")

    @staticmethod
    def get_directory_only(path):
        if not os.path.isdir(path):
            return os.path.dirname(path)

    @staticmethod
    def get_file_name(path):
        if not os.path.isdir(path):
            return os.path.splitext(os.path.basename(path))[0].split(".")[0]

    @staticmethod
    def get_file_extension(path):
        extensions = []
        copy_path = path
        while True:
            copy_path, result = os.path.splitext(copy_path)
            if result != '':
                extensions.append(result)
            else:
                break
        extensions.reverse()
        return "".join(extensions)

    @staticmethod
    def get_files_in_dir(dir_path):
        # list to store files
        res = []
        for file_path in os.listdir(dir_path):
            if os.path.isfile(os.path.join(dir_path, file_path)):
                first_word = file_path.split('_')[0]
                if first_word == "pool":
                    res.append(file_path)
        return res

    @staticmethod
    def get_all_text_files_in_dir(dir_path):
        # list to store files
        res = []
        for file_path in os.listdir(dir_path):
            if os.path.isfile(os.path.join(dir_path, file_path)):

                if file_path.endswith('.txt'):   # check only text files
                    res.append(file_path)
        return res

    @staticmethod
    def create_dir_if_not_exists(dir_path):
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

    @staticmethod
    def create_file_if_not_exists(file_path):
        if not os.path.exists(file_path):
            # print("File do not exist, hence created")
            file_handle = open(file_path, "w+")
        else:
            # print("File exists already, creating a new")
            file_handle = open(file_path, 'w+')

        return file_handle

    @staticmethod
    def get_one_dir_up(dir_name):
        return str(Path(dir_name).parents[0])  # get one level up in the directory
