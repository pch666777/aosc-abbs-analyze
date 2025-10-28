import os
import logging
import findDB


def MainRun():
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s %(message)s',
                        datefmt='%H:%M:%S',
                        handlers=[logging.StreamHandler()])
    while True:
        action = input("anan: ")
        aclist = [item for item in action.split(" ") if item != ""]
        if len(aclist) == 0:
            continue
        if aclist[0] == "exit" or aclist[0] == "quit":
            break
        if aclist[0] == "find-deps":
            FindDeps(aclist)
        else:
            print("未知的操作: " + aclist[0])
        #end-if
        pass
    #end-while
    pass
#end-def

def FindDeps(aclist):
    workDir = "/home/pngchs/build/amd64/TREE"
    findDB.create_db(workDir)
    pass
#end-def

# =================================================
workDir = os.getcwd()

print("=========使用说明=========")
print("所有分析的结果都是基于本地 abbs 树，无任何其他分析")
print("当前的工作目录是: " + workDir)
print("用法1: find-deps xxxx to csv 表示按层级列出xxxx包的依赖，并导出为csv文件")
print("用法2: exit 退出程序\n")

MainRun()