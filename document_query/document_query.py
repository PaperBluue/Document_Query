import os
import re
import docx
import time
import requests

classmates = {0: "tmp"
              }  # 班级同学信息

ord_path: str = str()  # 文件路径
rollCall_path: str = str()  # 读取名单文件路径
sinput_path: str = str()  # 读取被查询文件路径
ExistList_path: str = str()  # 输出查询结果文件路径
Panbaidu_dir: str = str()  # 查询的百度盘的文件夹的路径

rc_mode = 2  # rc_mode：被读取的文本如果是”学号 姓名“就用2。1的情况没写完，看缘分吧。
dealmode = "filename"  # 选择处理文件信息的方式
Exist = True  # 是否打印已交人数
Exist_more = False  # 是否打印已交人数名单
NonExist = True  # 是否打印未交人数
NonExist_more = False  # 是否打印未交人数名单

AppKey = ""  # 无需修改
access_token = ""  # 有效期一个月，访问url_get_access_token获取新的access_token
url_get_access_token = ""

allnums = []  # 原班级学号列表，处理后即未交同学学号列表
filenames = []  # 文件夹内所有的文件的文件名列表
existnums = []  # 已交的同学的学号
outOfClass = []  # 班外同学
filenames_time = []  # 记录每个文件的时间
allnums_count = {}  # 记录每个人的提交次数，多文件提交时间列表，最后一次提交时间
s_input = """
"""


def init(**kwargs):
    """
    初始化

    :return: None
    """
    global ord_path, allnums, filenames, \
        existnums, outOfClass, rollCall_path, sinput_path, \
        s_input, ExistList_path, Panbaidu_dir, allnums_count

    allnums.clear()  # 清空列表
    filenames.clear()
    existnums.clear()
    outOfClass.clear()
    allnums_count.clear()
    ord_path = ""  # 清空字符串
    rollCall_path = ""
    sinput_path = ""
    ExistList_path = ""
    Panbaidu_dir = ""

    if kwargs.get("files_path", False):
        ord_path = kwargs.get("files_path", ord_path)  # 文件路径
        files = os.scandir(ord_path)  # 获取所有文件信息
        filenames = [i.name for i in files]  # 文件夹内所有的文件的文件名列表
    if kwargs.get("rc_path", False):
        rollCall_path = kwargs.get("rc_path", rollCall_path)
        read_rollCall()
    if kwargs.get("s_path", False):
        sinput_path = kwargs.get("s_path", sinput_path)
        s_input = read_input(s_path)
    if kwargs.get("existlist_path", False):
        ExistList_path = kwargs.get("existlist_path", ExistList_path)
    if kwargs.get("panbaidu_path", False):
        Panbaidu_dir = kwargs.get("panbaidu_path", Panbaidu_dir)
        get_baidu_path_filenames()
        ord_path = "baidu/" + Panbaidu_dir

    allnums = [int(i) for i in classmates.keys()] \
        if rc_mode == 2 else [i for i in classmates.values()]  # 原班级学号列表，处理后即未交同学学号列表
    for i in allnums:
        allnums_count[i] = {"count": 0,
                            "times": [0],
                            "latest_time": ""
                            }


def f_dealAll():
    """
    根据文件名进行数据处理

    :return: None
    """
    for i in range(len(filenames)):
        # print(re.findall(r'[1-9]+\.?[0-9]*', i.name)[0])
        try:
            filename_num = int(re.findall(r'[1-9]+\.?[0-9]*', filenames[i])[0])
        except:
            filename_num = 0
        # noinspection PyBroadException
        try:
            allnums.remove(filename_num)  # 剔除已交的同学
            allnums_count[filename_num]["count"] += 1
            allnums_count[filename_num]["times"].append(filenames_time[i])

            filename_num = str(filename_num)
            filename_num = '0' + filename_num if len(filename_num) != 9 else filename_num
            existnums.append(filename_num)  # 添加已提交同学
        except:
            if filename_num in allnums_count:
                allnums_count[filename_num]["count"] += 1
                allnums_count[filename_num]["times"].append(filenames_time[i])
            else:
                outOfClass.append(filenames[i])  # 添加班外或错误内容

    for i in allnums_count.keys():
        allnums_count[i]["latest_time"] = \
            time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(max(allnums_count[i]["times"])))

    pass


def f_dealAll_data():
    """
    根据文件内容进行数据处理,当使用百度云文件夹查询时可能会出现问题\n
    ord_path不合理还需要调整,已做应急处理\n
    目前的解决方案就是在度盘查询的时候别用这个方法

    :return: None
    """
    if "baidu" in ord_path:
        pass
    else:
        for name in filenames:
            tmppath = rf"{ord_path}\{name}"
            # print(tmppath)
            file = docx.Document(tmppath)
            for i in range(50):
                tmp = file.paragraphs[i].text.replace(" ", "")
                # print(tmp)
                for k in classmates.keys():
                    if classmates[k] in tmp:
                        if k in existnums:
                            pass
                        else:
                            existnums.append(k)
                    else:
                        pass
        for i in existnums:
            if int(i) in allnums:
                allnums.remove(int(i))


def printAllNum():
    """
    打印总人数和作业

    :return: None
    """
    if "baidu" in ord_path:
        name = ord_path.split('/')[-1]
        pass
    else:
        name = ord_path.split('\\')[-2] + " " + ord_path.split('\\')[-1]
    print(f'本次查询的是 {name}\n应提交人数{len(classmates.keys())}人\n')  # 打印总人数和作业


def printExist(**kwargs):
    """
    打印已交作业同学人数，名单可选

    :param kwargs: more: True即打印名单
    :return: None
    """
    print(f'已经交了{len(existnums) + len(outOfClass)}人', end="")  # 打印已交人数
    print(f'，班内{len(existnums)}人，班外{len(outOfClass)}人', end="") if len(outOfClass) != 0 else None
    tmp_repeat = {
        "num_people": 0,
        "num_file": 0
    }
    for i in allnums_count.keys():
        if allnums_count[i]["count"] > 1:
            tmp_repeat["num_people"] += 1
            tmp_repeat["num_file"] += allnums_count[i]["count"] - 1
    if tmp_repeat["num_people"] != 0:
        print(f'\n有{tmp_repeat["num_people"]}人重复提交，有{tmp_repeat["num_file"]}份重复文件')

    if len(outOfClass) != 0:
        print('班外同学是：')
        for i in outOfClass:
            print(i)
        pass

    if kwargs.get('more', False):
        print('，这些同学是：')
        for i in existnums:
            print(i, classmates[i])  # 打印已交同学学号姓名


# noinspection PyTypeChecker
def printNonExist(**kwargs):
    """
    打印未交作业同学人数，名单可选

    :param kwargs: more: True即打印名单
    :return: None
    """
    print(f'\n还有{len(allnums)}人没交', end="")  # 打印未交人数
    if kwargs.get('more', False):
        print('，这些人是：')
        if rc_mode == 2:
            for i in allnums:
                i = str(i)
                i = '0' + i if len(i) == 8 else i
                print(i, classmates[i])  # 打印未交同学的学号姓名
        elif rc_mode == 1:
            for i in allnums:
                print(i)


# noinspection PyTypeChecker
def s_dealAll():
    """
    根据输入文本进行数据处理，仅筛选本班

    :return:
    """
    for i in allnums:
        if rc_mode == 2:
            if (str(i) in s_input) or (classmates['0' + str(i) if len(str(i)) == 8 else str(i)] in s_input):
                existnums.append(i)
            else:
                pass
        elif rc_mode == 1:
            if str(i) in s_input:
                existnums.append(i)
            else:
                pass
    for i in existnums:
        if i in allnums:
            allnums.remove(i)
    pass


# noinspection PyTypeChecker
def read_rollCall():
    """
    读取txt文本中的外部输入名单，原来默认的本班名单会被清空

    :return: None
    """
    global classmates, rc_mode
    if len(rollCall_path) == 0:
        print("rollCall_path error")
        return 0
    else:
        classmates.clear()  # 清空字典
        pass

    f = open(rollCall_path, encoding="UTF-8")
    line = f.readline().strip()  # 读取第一行
    rc_mode = 2 if " " in line else 1
    txt = [line]
    while line:  # 直到读取完文件
        line = f.readline().strip()  # 读取一行文件，包括换行符
        txt.append(line)
    f.close()  # 关闭文件
    if rc_mode == 2:
        for i in txt:
            tmp = i.split(" ")
            if len(tmp) == 2:
                classmates[tmp[0]] = tmp[1]
    elif rc_mode == 1:
        cnt = 0
        for i in txt:
            if i != '':
                classmates[str(cnt)] = i
                cnt += 1
        pass


def read_input(path: str = None):
    f = open(path, encoding="UTF-8")
    txt_tmp = f.read()
    f.close()
    return txt_tmp


def debug():
    # print(classmates)
    # print(len(classmates))
    # printAllNum()
    pass


def deal_top():
    global dealmode, Exist, Exist_more, NonExist, NonExist_more
    if dealmode == "filename":
        f_dealAll()
    elif dealmode == "filedata":
        f_dealAll_data()
    elif dealmode == "s_input":
        s_dealAll()


def print_top():
    printAllNum()
    if Exist:
        printExist(more=Exist_more)
    if NonExist:
        printNonExist(more=NonExist_more)


def update_top(**kwargs):
    update_ExistList() if ExistList_path else None
    update_NonExistList() if kwargs.get("update_NonExistList", False) else None


def update_ExistList():
    # print(filenames)
    with open(ExistList_path, "w") as f:
        f.writelines('本文件最后一次更新时间是 ' + time.strftime('%b %d %H:%M:%S %Y\n', time.localtime()))
        if len(allnums) == 0:
            f.writelines("所有同学都完成文件提交，感谢大家的配合！！！\n")
            f.writelines("以下是已提交文件的同学名单：\n")
        else:
            f.writelines(f"已提交{len(existnums)}人，还有{len(allnums)}人未提交。\n以下是已提交文件的同学名单：\n")
        f.writelines("学号 姓名 提交次数 最后一次提交的文件的时间\n")
        for i in existnums:
            name = classmates[i] + "  " if len(classmates[i]) == 2 else classmates[i]

            f.writelines(
                i + " " +
                name + " " +
                str(allnums_count[int(i)]["count"]) + " " +
                str(allnums_count[int(i)]["latest_time"]) +
                "\n"
            )

        if len(outOfClass) != 0:
            f.writelines(f"\n本次查询中找到不在被查询名单的同学提交的文件，该文件是：\n")
            for i in outOfClass:
                f.writelines(f"{i}\n")
            f.writelines("请上传以上文件的同学联系我(QQ:2440075307)，可能是我的查询名单有缺漏或者是其他原因。\n\n")

        f.writelines("本文件已实现每五分钟自动更新，只要我的电脑开着。"
                     "\n如果发现自己已提交文件但长时间未出现在名单中，请私聊我(QQ:2440075307)\n")
    pass


# noinspection PyTypeChecker
def update_NonExistList():
    tmpstrlist = list(ExistList_path)
    tmpstrlist.insert(-4, "1")
    with open("".join(tmpstrlist), "w") as f:
        f.writelines('本文件最后一次更新时间是 ' + time.strftime('%b %d %H:%M:%S %Y\n', time.localtime()))
        f.writelines(f"已提交{len(existnums)}人，还有{len(allnums)}人未提交。\n以下是未提交文件的同学名单：\n")
        if rc_mode == 2:
            for i in allnums:
                i = str(i)
                i = '0' + i if len(i) == 8 else i
                f.writelines(i + " " + classmates[i] + "\n")
        elif rc_mode == 1:
            for i in allnums:
                f.writelines(i + " " + classmates[i] + "\n")
        f.writelines("本文件已实现每五分钟自动更新，只要我的电脑开着。"
                     "\n如果发现自己已提交文件但长时间未出现在名单中，请私聊我(QQ:2440075307)\n")
    pass


# noinspection PyTypeChecker
def update_ExistAndNoneList():
    with open(ExistList_path, "w") as f:
        f.writelines('本文件最后一次更新时间是 ' + time.strftime('%b %d %H:%M:%S %Y\n', time.localtime()))
        f.writelines(f"已提交{len(existnums)}人，还有{len(allnums)}人未提交。\n以下是已提交文件的同学名单：\n")
        for i in existnums:
            f.writelines(i + " " + classmates[i] + "\n")
        f.writelines("\n以下是未提交文件的同学名单：\n")
        if rc_mode == 2:
            for i in allnums:
                i = str(i)
                i = '0' + i if len(i) == 8 else i
                f.writelines(i + " " + classmates[i] + "\n")
        elif rc_mode == 1:
            for i in allnums:
                f.writelines(i + " " + classmates[i] + "\n")

        f.writelines("本文件已实现每五分钟自动更新，只要我的电脑开着。"
                     "\n如果发现自己已提交文件但长时间未出现在名单中，请私聊我(QQ:2440075307)\n")
    pass


def get_baidu_path_filenames():
    """
    获取百度云文件夹中的文件清单。\n
    如果遇到access_token失效则打开url_get_access_token中的网址获取新的access_token。\n
    如遇问题则访问 https://pan.baidu.com/union/console/applist\n

    :return:
    """

    global Panbaidu_dir, access_token, filenames, filenames_time
    url = f"https://pan.baidu.com/rest/2.0/xpan/file?method=list&dir={Panbaidu_dir}&order=name&start=0&web=0&folder=0&access_token={access_token}"
    payload = {}
    files_list = {}
    headers = {
        'User-Agent': 'pan.baidu.com'
    }
    response = requests.request("GET", url, headers=headers, data=payload, files=files_list)
    tmp_list = eval(response.text.encode('utf8').decode())['list']
    filenames = [i["server_filename"] for i in tmp_list]
    filenames_time = [int(i["server_mtime"]) for i in tmp_list]


def clear_NonExistList():
    tmpstrlist = list(ExistList_path)
    tmpstrlist.insert(-4, "1")
    try:
        os.remove("".join(tmpstrlist))
    except:
        pass
    pass


class init_datas:
    """
    增强复用性，如果同时又多份作业同时收可以使用这个类记录信息

    """

    def __init__(self, files_path=None, rc_path=None, s_path=None, existlist_path=None, panbaidu_path=None):
        self.files_path = files_path
        self.rc_path = rc_path
        self.s_path = s_path
        self.existlist_path = existlist_path
        self.panbaidu_path = panbaidu_path
        pass

    pass


def init_from_class(datas: init_datas):
    """
    使用init_datas来初始化，增强复用性

    :param datas: 用于查询的信息
    :return:
    """
    init(
        files_path=datas.files_path,  # 被查询的文件夹路径
        rc_path=datas.rc_path,  # 外部名单输入，没有的话就None
        s_path=datas.s_path,
        existlist_path=datas.existlist_path,
        panbaidu_path=datas.panbaidu_path
    )


class datass:
    """
    暂时的顶层模块

    """

    def __init__(self, *args: init_datas):
        self.data_list = []
        if len(args) != 0:
            for i in args:
                self.data_list.append(i)
        self.if_clear_NonExistList = False
        pass

    def data_append(self, *args: init_datas):
        for i in args:
            self.data_list.append(i)

    def data_remove(self, *args: init_datas):
        """
        说实话我其实不太想加上这玩意我觉得这很蠢\n
        :param args:
        :return:
        """
        for i in args:
            self.data_list.remove(i)

    def data_remove_all(self):
        self.data_list.clear()

    def progress_all(self):
        print("本轮查询时间是", time.strftime('%b %d %H:%M:%S %Y\n', time.localtime()))
        for i in self.data_list:
            print("--------查询开始--------")

            init_from_class(i)
            deal_top()
            print_top()
            update_top(update_NonExistList=False)

            if self.if_clear_NonExistList:
                clear_NonExistList()
            print("\n--------查询结束--------\n\n")

    pass
