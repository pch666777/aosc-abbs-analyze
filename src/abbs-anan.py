import os
import json
import logging
import findDB


def MainRun():
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s %(message)s',
                        datefmt='%H:%M:%S',
                        handlers=[logging.StreamHandler()])
    workDir = "/home/pngchs/build/amd64/TREE"
    if not os.path.exists(os.path.join(workDir, "groups")):
        logging.error("没有找到groups目录！请确保工作路径为abbs目录！")
        return
    findDB.create_db(workDir)
    # 导出为JSON
    outFile = os.path.join(os.path.expanduser("~"), "abbs.json")
    logging.info("输出文件:%s" % outFile)
    with open(outFile, "w", encoding="utf-8") as f:
        json.dump(findDB.abbsDB, f)
    #end-with
    logging.info("执行完成")
#end-def

# =================================================
workDir = os.getcwd()

print("=========使用说明=========")
print("分析本地`abbs`树，转化为json文件，使用网页加载数据分析")
print("当前的工作目录是: " + workDir)
MainRun()