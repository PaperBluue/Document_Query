import document_query

document_query.AppKey = ""  # 无需修改
document_query.access_token = ""  # 有效期一个月，访问url_get_access_token获取新的access_token
document_query.url_get_access_token = ""

datas_1 = document_query.init_datas(
    rc_path="",
    existlist_path="",
    panbaidu_path=""
)


top = document_query.datass()
top.data_append(datas_2, datas_3, datas_4)
top.progress_all()
