import os
import logging
import subprocess
# 扫描得到的结果存储在这，包名应该是唯一的
abbsDB = {}
# 用于标识输出的分割符号
divSym = "+++###+++"

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
            #break
        #end-if
    #end-for
    logging.info("分析数据...")
#end-def
        
def find_abbs_package_file(dirpath: str, dirnames: list[str]):
    # dirpath = "/home/pngchs/build/amd64/TREE/runtime-gis/pdal"
    # dirnames = ["autobuild"]
    # 进入spec 的下层目录，查找 define 文件
    for thisDir in dirnames:
        defile = os.path.join(dirpath, thisDir)
        defile = os.path.join(defile, "defines")
        if os.path.exists(defile):
            package = parser_file(defile)
            if "PKGNAME" in package.keys():
                abbsDB[ package["PKGNAME"] ] = package
            else:
                logging.error("没有包名: %s" % defile)
            #end-if
        #end-if
    #end-for
#end-if

def analyze_package(pkg: str):
    pass
#end-def
                

## ================ 解析文件 ==================
def parser_file(fn: str):
    with open(fn, 'r') as file:
        context = file.read()
    #end-with
    max = len(context)
    # 先查找需要的关键字
    outKey = get_key_words(context, max)
    # 提取的关键字附加到 defines 输出
    newcontext = attach_to_defines(context, outKey)
    # 执行
    result = subprocess.run(newcontext, shell=True, timeout=10, capture_output=True, text=True)
    # print(result.stdout)
    # 把 ++++ 中的内容解析出来
    out, err = tranz_result_to_map(result.stdout, outKey)
    if len(err) > 0:
        logging.error("解析遇到错误:%s" % fn)
        for e in err:
            logging.error(e)
        #end-for
    #end-if
    return out
#end-def

# 查找所有有效的关键字
def get_key_words(context: str, max: int):
    baseKey = ["PKGNAME", "PKGDEP", "BUILDDEP"]
    outKey = []
    for key in baseKey:
        current = 0
        # 找到所有以关键字开头的单词
        while current < max and current >= 0:
            pos = context.find(key, current)
            if pos < 0:
                break  # 关键字单词找完了
            #end-if
            word, current = get_word(context, pos, max)
            outKey.append(word)
            #logging.debug("key is: %s" % word)
        #end-while
    #end-for
    return outKey
#end

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

# 附加到输出
def attach_to_defines(context: str, outKeys: list[str]):
    if len(outKeys) == 0:
        return context
    lst = []
    lst.append('echo "%s"' % divSym)
    for key in outKeys:
        lst.append('echo "%s"' % key)
        lst.append('echo "%s"' % divSym)
        lst.append('echo "$%s"' % key)
        lst.append('echo "%s"' % divSym)
    #end-for
    return context + "\n" + str.join("\n", lst)
#end-def

# 提取其中有效的输出，转化为字典
def tranz_result_to_map(result: str, outKey: list[str]):
    tls = []
    out = {}
    err = []
    if result is None:
        return out, err
    max = len(result)
    divlen = len(divSym)
    current = 0
    while current < max:
        startpos = result.find(divSym, current)
        # 超出范围的
        if startpos < 0 or startpos + divlen >= max:
            break
        # 下一个标记
        endpos = result.find(divSym, startpos + divlen)
        if endpos < 0:
            break
        word = result[current + divlen:endpos].strip()
        tls.append(word)
        #logging.debug("word is:%s" % word)
        current = endpos
    #end-while
    count = len(tls)
    if count % 2 == 1:
        err.append("变量与值的数量不匹配！")
    if count != (len(outKey) * 2):
        err.append("输入关键字与输出关键字的数量不匹配！")
    #end-if
    ii = 0
    while ii < count:
        if ii + 1 < count:
            out[tls[ii]] = tls[ii+1]
            ii += 2
        else:
            out[tls[ii]] = "error"
            ii += 1
        #end-if
    #end-while
    return out, err
#end-def

# 返回下一行的位置
def next_line_position(context, pos, max):
    while pos < max:
        if context[pos] == '\n':
            return pos + 1
        else:
            pos += 1
        #end-if
    #end-while
    return max
#end-def