from flask import Flask, Blueprint, request, jsonify, render_template
from util.post_response import get_return_response

blog_manage = Blueprint("blog_manage", __name__)


@blog_manage.route('/to_blog_manage')
def to_blog_manage():
    """去博客列表页
    :return:博客列表页模板
    """
    return render_template("blog_manage/blog-manage-list.html")


@blog_manage.route('/get_blog_manage_list', methods=['Post', ])
def get_blog_manage_list():
    """
    获取博客列表页的datatable的数据
    :return:
    """
    form = request.form
    sEcho = int(form.get('sEcho')) + 1
    iDisplayStart = int(form.get('iDisplayStart'))
    iDisplayLength = int(form.get('iDisplayLength'))
    currentPage = iDisplayStart / iDisplayLength + 1

    # 构造datables插件需要的配置数据
    response_datatables = {}
    response_datatables['sEcho'] = sEcho
    response_datatables['draw'] = currentPage
    response_datatables['recordsFiltered'] = 1
    response_datatables['recordsTotal'] = 1


    # 构造返回的data
    response_data = {}
    response_data['id'] = 1
    response_data['title'] = 1
    response_data['describle'] = 1
    response_data['big_label'] = 1
    response_data['small_label'] = 1
    response_data['url'] = 1
    response_data['create_time'] = 1
    response_data['update_time'] = 1
    response_data['hits'] = 1
    response_data['is_status'] = 1

    response_datatables['data'] = response_data
    print(response_datatables)
    response = get_return_response(jsonify(response_datatables))
    return response
