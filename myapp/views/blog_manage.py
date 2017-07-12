import time

from flask import Blueprint, request, jsonify, render_template
import time
# mongodb数据库连接
from connect_db.connect_mongo import ConnectMongoDB,ObjectId
# from ueditor import UEditor
from util.post_response import get_return_response

blog_manage = Blueprint("blog_manage", __name__)

# app = Flask(__name__)
# ue = UEditor(app)

connection = ConnectMongoDB()  # 连接数据库
blog_collection = connection.get_collection('blog')  # 博客表
blog_label_collection = connection.get_collection('blog_label')  # 博客标签表


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
    form = request.form
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
    response_data_array = []
    for response_data in result:
        response_data['_id'] = str(response_data['_id'])
        response_data_array.append(response_data)

    response_datatables['data'] = response_data_array
    print(response_datatables)
    response = get_return_response(jsonify(response_datatables))
    return response


@blog_manage.route('/to_blog_add')
def to_blog_add():
    """
    去博客新增页
    :return:
    """

    return render_template("blog_manage/article-add.html")

@blog_manage.route('/get_taglist', methods=['Post', 'Get'])
def get_taglist():
    '''
    获取博客标签列表
    :return:
    '''
    print("标签列表")
    result_taglist=connection.find_data(blog_label_collection,{"is_del":0})
    response_data_array = []
    for response_data in result_taglist:
        response_data['_id'] = str(response_data['_id'])
        response_data_array.append(response_data)
    print(response_data_array)
    response = get_return_response(jsonify(response_data_array))
    return response


@blog_manage.route('/save_blog', methods=['POST', 'GET'])
def save_blog():
    """
    保存博客
    :return:
    """
    form = request.form
    title = form.get('title')
    onetype = form.get('onetype')
    twotype = form.get('twotype')
    maincontent = form.get('maincontent')
    content = form.get('content')
    info = {}
    info['title'] = title  # 标题
    info['big_label_id'] = onetype.split("@")[0]  # 一级分类
    info['big_label_name'] = onetype.split("@")[1]  # 一级分类名称
    info['small_label_id'] = twotype.split("@")[0]  # 二级分类
    info['small_label_name'] = twotype.split("@")[1]  # 二级分类名称
    info['content'] = content  # 内容
    info['describe'] = maincontent  # 概要
    info['is_status'] = 0  # 0未发布
    info['create_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))  # 创建时间
    info['update_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))  # 更新时间
    info['title_img_url'] = ''  # 标题图片
    info['url'] = ''  # 博客静态页
    info['hits'] = 0  # 点击次数
    info['is_top'] = False  # 是否置顶
    print(info['create_time'], info['title'])
    connection.insert_list(blog_collection, info)
    response = get_return_response(jsonify({"status": 1}))
    return response