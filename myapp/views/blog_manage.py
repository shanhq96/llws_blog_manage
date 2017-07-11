from flask import Flask, Blueprint, request, jsonify, render_template
from util.post_response import get_return_response
# mongodb数据库连接
from connect_db.connect_mongo import ObjectId, ConnectMongoDB

blog_manage = Blueprint("blog_manage", __name__)

connection = ConnectMongoDB()  # 连接数据库
blog_collection = connection.get_collection('blog')


@blog_manage.route('/to_blog_manage')
def to_blog_manage():
    """去博客列表页
    :return:博客列表页模板
    """
    return render_template("blog_manage/blog-manage-list.html")


@blog_manage.route('/get_blog_manage_list', methods=['Post', 'Get'])
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

    # 查询数据库
    result_temp = connection.find_data(blog_collection)
    result = result_temp.skip(data_start).limit(data_length)

    # 构造datables插件需要的配置数据
    response_datatables = {}
    response_datatables['draw'] = draw
    response_datatables['recordsFiltered'] = result_temp.count()
    response_datatables['recordsTotal'] = result_temp.count()

    # 构造返回的data
    ii = data_start
    response_data_array = []
    for response_data in result:
        ii += 1
        response_data['_id'] = str(response_data['_id'])
        # response_data = {}
        # response_data['id'] = i
        response_data['title'] = ii
        response_data['describe'] = ii
        response_data['big_label'] = ii
        response_data['small_label'] = ii
        response_data['url'] = ii
        response_data['create_time'] = ii
        response_data['update_time'] = ii
        response_data['hits'] = ii
        response_data['is_top'] = ii<4
        response_data['is_status'] = 1
        response_data_array.append(response_data)

    response_datatables['data'] = response_data_array
    print(response_datatables)
    response = get_return_response(jsonify(response_datatables))
    return response
