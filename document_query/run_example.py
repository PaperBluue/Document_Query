# 导库
import document_query

# 如果不用度盘查询可以忽略段代码--------------------
# 这俩玩意是用于获取access_token，在代码中用不到
document_query.AppKey = ""
document_query.url_get_access_token = ""
# 必要的token
document_query.access_token = ""
# ____________________________________________

# 查询的基本信息保存对象，如果有多个查询需求就可直接再创建一个
datas_1 = document_query.init_datas(
    # 其中只有rc_path是必填项，其他都是可选项
    # 被查询的文件夹路径
    files_path=None,
    # 被查询的文件的路径
    s_path=None,
    # 被查询的度盘文件夹路径
    panbaidu_path=None,
    # 输出查询结果的文件路径
    existlist_path=None,
    # 查询名单路径
    rc_path=None,
    # 重复文件筛选清单路径
    duplicate_file_path=None
)

# 创建顶层对象
top = document_query.datass()
# 把创建的基本信息保存对象全部添加导顶层模块中
top.data_append(datas_1)


# 开始

def run_data():
    top.progress_all()


def switch_NonExist_more():
    document_query.NonExist_more = ~document_query.NonExist_more
    print(f"此时是否打印未交名单？{bool(document_query.NonExist_more)}")


def switch_Exist_more():
    document_query.Exist_more = ~document_query.Exist_more
    print(f"此时是否打印已交名单？{bool(document_query.Exist_more)}")


def show_NonExist_more():
    print(f"未交名单：{bool(document_query.NonExist_more)}")
    print(f"已交名单：{bool(document_query.Exist_more)}")


if __name__ == '__main__':
    top.progress_all()
