from flask import Flask, Blueprint, request, jsonify, render_template
# from ueditor import UEditor
from util.post_response import get_return_response

blog_manage = Blueprint("blog_manage", __name__)
# app = Flask(__name__)
# ue = UEditor(app)

@blog_manage.route('/to_blog_add')
def to_blog_add():
    return render_template("blog_manage/article-add.html")



@blog_manage.route('/to_blog_manage')
def to_blog_manage():
    """去博客列表页
    :return:博客列表页模板
    """
    return render_template("blog_manage/blog-manage-list.html")


@blog_manage.route('/get_blog_manage_list', methods=['Post','Get' ])
def get_blog_manage_list():
    """
    获取博客列表页的datatable的数据
    :return:
    """
    test_totle_data_num = 75

    form = request.form
    print(form)
    data_start = int(form.get('start'))
    data_length = int(form.get('length'))
    currentPage = data_start / data_length + 1
    draw = int(form.get('draw'))

    # 构造datables插件需要的配置数据
    response_datatables = {}
    response_datatables['draw'] = draw
    response_datatables['recordsFiltered'] = test_totle_data_num
    response_datatables['recordsTotal'] = test_totle_data_num


    # 构造返回的data
    response_data_array = []
    for i in range(test_totle_data_num):
        response_data = {}
        response_data['id'] = i
        response_data['title'] = 1
        response_data['describle'] = 1
        response_data['big_label'] = 1
        response_data['small_label'] = 1
        response_data['url'] = 1
        response_data['create_time'] = 1
        response_data['update_time'] = 1
        response_data['hits'] = 1
        response_data['is_top'] = 1
        response_data['is_status'] = 1
        response_data_array.append(response_data)



    response_datatables['data'] = response_data_array
    print(response_datatables)
    response = get_return_response(jsonify(response_datatables))
    return response