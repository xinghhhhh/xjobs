import os
import configparser
import importlib
import inspect
import sys

config = configparser.ConfigParser()
config.read("D:\\code\\python\\xjobs\\common\\config\\common.ini", encoding="utf-8")

def scan_file(directory, prefix=None, postfix=".py"):
    file_list = []
    for root,sub_dirs,files in os.walk(directory):
        for special_file in files:
            if postfix:
                if special_file.endswith(postfix):
                    file_list.append(os.path.join(root, special_file))
            elif prefix:
                if special_file.startswith(prefix):
                    file_list.append(os.path.join(root, special_file))
            else:
                file_list.append(os.path.join(root, special_file))
    return file_list

def get_module_by_file(file_easy_name):
    file_easy_name = file_easy_name[21:-3].replace('\\', '.')
    return importlib.import_module(file_easy_name)

def get_classes_by_module(module):
    cls_list = []
    for name, class_ in inspect.getmembers(module, inspect.isclass):
        cls_list.append(class_())
    return cls_list

def get_classes_by_file(file_name):
    file_easy_name = file_name[21:-3].replace('\\', '.')
    module = importlib.import_module(file_easy_name)
    cls_list = []
    for name, class_ in inspect.getmembers(module, inspect.isclass):
        cls_list.append(class_())
        class_().run()
    return cls_list

file_list = scan_file("D:\\code\\python\\xjobs\\jsyh\\jobs",None,".py")
for file in file_list:
    module = get_module_by_file(file)
    classes = get_classes_by_module(module)
    for cls in classes:
        print(cls.run("46546"))
