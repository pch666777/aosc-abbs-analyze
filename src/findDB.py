import os
import logging

# 扫描得到的结果存储在这，包名应该是唯一的
abbsDB = {}

def create_db(workdir: str):
    currentdir = workdir
    if not os.path.exists(currentdir):
        raise Exception("指定的路径不存在: %s" % currentdir )
    #end-if
    logging.info("扫描数据...")
    for dirpath, dirnames, filenames in os.walk(currentdir):
        # 当前目录有 spec 文件，下一层级目录才是符合条件的
        if "spec" in filenames:
            #logging.debug("找到 spec 文件在: %s" % dirpath)
            find_abbs_package_file(dirpath, dirnames)
            break
        #end-if
    #end-for
#end-def
        
def find_abbs_package_file(dirpath: str, dirnames: str):
    # 进入spec 的下层目录，查找 define 文件
    for thisDir in dirnames:
        defile = os.path.join(dirpath, thisDir)
        defile = os.path.join(defile, "defines")
        if os.path.exists(defile):
            package = parser_file(defile)
            if "PKGNAME" in package.keys():
                abbsDB[ package["PKGNAME"] ] = package
            else:
                logging.error("解析错误: %s" % defile)
            #end-if
        #end-if
    #end-for
#end-if
                

## ================ 解析文件 ==================
def parser_file(fn: str):
    with open(fn, 'r') as file:
        context = file.read()
    #end-with
    out = {}
    wordStark = []
    symbolStark = []
    max = len(context)
    current = 0
    while current <= max:
        # 注释直接下一行
        if context[current] == '#':
            current = next_line_position(context, current + 1, max)
            continue
        #end-if
        # 字母或者 _ 开头则认为是一个单词的开头
        if context[current].isalpha() or context[current] == '_':
            word, current = get_word(context, current, max)
            pass
        #end-if

    #end-while
    return out
#end-def

# 返回下一行的位置
def next_line_position(context, pos, max):
    while pos < max:
        if context[pos] == '\n':
            # \r 和 \n 按同样的模式处理，以防出错
            while (context[pos] == '\n' or context[pos] == '\r') and pos < max:
                pos += 1
            #end-while
            return pos
        else:
            pos += 1
        #end-if
    #end-while
    return max
#end-def

# 返回一个单词，只能是字母、下划线、-、数字的组合
def get_word(context: str, pos: int, max: int):
    start = pos
    pos += 1
    while pos < max:
        ccc = context[pos]
        if ccc.isalpha() or ccc.isdecimal() or ccc == '-' or ccc == '_':
            pos += 1
        else:
            return context[start:pos], pos
        #end-if
    return context[start:max], max
#end-def