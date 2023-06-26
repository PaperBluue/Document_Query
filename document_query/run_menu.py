try:
    import run
except:
    import run_example as run
import time
from func_timeout import func_set_timeout, FunctionTimedOut
import os


def clear():
    os.system('cls')


@func_set_timeout(2)
def input_catch():
    if input() == "q":
        # print(111)
        return 1


Circulation_times = 300

while True:
    clear()
    print('-------------------------------------')
    print('        让我康康谁的作业不在这？     ')
    print('-------------------------------------')
    print('')
    print('[0]: 单次查询')
    print('[1]: 循环查询')
    print('[2]: 更改参数')
    print('[3]: 显示此时参数')
    n = input('>>> 请输入编号选择模式, 输入q退出程序\n>>> ')
    if n == "":
        n = 0
    elif n == "q":
        break
    try:
        n = int(n)
        if n > 3:
            print('>>> 请输入一个小于3的整数')
            input()
            continue
    except:
        print('>>> 无法解析输入')
        input()
        continue

    if n == 0:
        run.run_data()
        input()

    elif n == 1:
        run.run_data()
        Flag_circulation = 1
        i = 1
        while Flag_circulation:
            if i >= Circulation_times + 1:
                print("\n\n\n")
                run.run_data()
                i = 1
            # print("离下次查询还有%d秒\n" % Circulation_times, end='')
            try:
                if input_catch():
                    print("成功退出循环查询")
                    Flag_circulation = 0
            except FunctionTimedOut as e:
                print(f"\r离下次查询还有{Circulation_times - i}秒        ", end='')
                pass
            i += 2
        input()

    elif n == 2:
        print('[0]: 更改循环查询时间')
        print('[1]: 切换是否输出未交名单')
        print('[2]: 切换是否输出已交名单')
        n2 = input('>>> 请输入编号选择模式, 输入q返回上级\n>>> ')
        if n2 == "":
            n2 = 0
        elif n2 == "q":
            continue
        try:
            n2 = int(n2)
            if n2 > 2:
                print('>>> 请输入一个小于3的整数')
                input()
                continue
        except:
            print('>>> 无法解析输入')
            input()
            continue

        if n2 == 0:
            flag_tmp = 1
            while flag_tmp:
                try:
                    Circulation_times = int(input("请输入更换的时间：\n>>>"))
                    flag_tmp = 0
                    print("此时循环查询时间为：", Circulation_times)
                except:
                    print("输入有误请更正")
        elif n2 == 1:
            run.switch_NonExist_more()
        elif n2 == 2:
            run.switch_Exist_more()
        input()
        pass

    elif n == 3:
        print("循环查询时间：", Circulation_times)
        run.show_NonExist_more()
        input()
