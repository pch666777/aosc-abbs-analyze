import os


def find_db(workdir: str, path: str):
    currentdir = workdir + "/" + path
    if not os.path.exists(currentdir):
        raise Exception("指定的路径不存在: %s" % currentdir )
    for dirpath, dirnames, filenames in os.walk(currentdir):
        print(f"当前目录: {dirpath}")
        print(f"子目录: {dirnames}")
        print(f"文件: {filenames}")
        print("-" * 20)
    #end-for
#end-def