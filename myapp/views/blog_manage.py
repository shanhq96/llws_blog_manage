import time

from flask import Blueprint, request, jsonify, render_template
import time
# mongodb数据库连接
from pymongo import ASCENDING, DESCENDING

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
    result = result_temp.skip(data_start).limit(data_length).sort("is_top", DESCENDING)

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


@blog_manage.route('/to_blog_label_manage')
def to_blog_label_manage():
    """
    去博客标签管理页
    :return:
    """
    return render_template("blog_manage/blog-label-manage-list.html")


@blog_manage.route('/get_blog_label_manage_list', methods=['Post', 'Get'])
def get_blog_label_manage_list():
    """
    获取项目标签列表的数据
    :return:符合datatable格式的数据
    """
    form = request.form
    data_start = int(form.get('start'))
    data_length = int(form.get('length'))
    currentPage = data_start / data_length + 1
    draw = int(form.get('draw'))

    # 查询数据库
    result_temp = connection.find_data(blog_label_collection, {"$and":[{"is_del":0}]})
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


@blog_manage.route('/to_blog_laebl_manage_add')
def to_blog_laebl_manage_add():
    """
    去博客标签新增页
    :return:
    """
    return render_template('blog_manage/blog-label-manage-add.html')


@blog_manage.route('/get_big_blog_label_list', methods=['Post', ])
def get_big_blog_label_list():
    """
    异步获取博客标签页的大标签数据
    :return:
    """
    response_datas = {}

    result = connection.find_data(blog_label_collection, {"$and":[{"label_type": 1},{"is_del":0}]})
    big_blog_labels = []
    for big_blog_label in result:
        big_blog_label['_id'] = str(big_blog_label['_id'])
        big_blog_labels.append(big_blog_label)
    response_datas['status'] = "success"
    response_datas['big_blog_labels'] = big_blog_labels
    response = get_return_response(jsonify(response_datas))
    return response


@blog_manage.route('/save_blog_label', methods=['Post', ])
def save_blog_label():
    """
    保存博客标签
    :return:
    """
    form = request.form
    blog_label_to_save = {}
    blog_label_to_save['label_name'] = form.get('label_name')  # 标签名称
    parent_label = form.get('parent_label')  # 大标签 id@name
    blog_label_to_save['parent_label_id'] = parent_label.split('@')[0]
    if (blog_label_to_save['parent_label_id'] == "0"):
        blog_label_to_save['label_type'] = 1  # 1代表大标签
        blog_label_to_save['parent_label_name'] = ''
    else:
        blog_label_to_save['label_type'] = 2  # 2代表小标签
        blog_label_to_save['parent_label_name'] = parent_label.split('@')[1]
    blog_label_to_save['create_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    blog_label_to_save['update_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    blog_label_to_save['is_del'] = 0
    connection.insert_list(blog_label_collection, blog_label_to_save)
    response = get_return_response(jsonify({"status": "success"}))
    return response


@blog_manage.route('/delete_blog_label',methods=['Post',])
def delete_blog_label():
    """
    删除博客标签,若为父标签,则会删除其下的全部子标签(即 将全部相关的标签的is_del均设置为1)
    :return:
    """
    form = request.form
    blog_label_to_del_id = form.get('blog_label_to_del_id')
    connection.update_data(blog_label_collection,{"$or":[{"_id":ObjectId(blog_label_to_del_id)},{"parent_label_id":blog_label_to_del_id}]},{"$set":{"is_del":1}},multi=True)
    response = get_return_response(jsonify({"status": "success"}))
    return response

@blog_manage.route('/blog_del',methods=['Post',])
def blog_del():
    '''
    删除博客
    :return:
    '''
    form = request.form
    blog_opetration_id = form.get('blog_opetration_id')
    connection.remove_one_data(blog_collection, {"_id": ObjectId(blog_opetration_id)})
    response = get_return_response(jsonify({"status": "success"}))
    return response


@blog_manage.route('/blog_top',methods=['Post',])
def blog_top():
    '''
    博客置顶
    :return:
    '''
    form = request.form
    blog_opetration_id = form.get('blog_opetration_id')
    if(connection.find_data(blog_collection,{"is_top":True}).count()<3):
        connection.update_data(blog_collection,{"_id":ObjectId(blog_opetration_id)},{"$set":{"is_top":True}},multi=True)
        response = get_return_response(jsonify({"status": "success"}))
    else:
        response = get_return_response(jsonify({"status": "fail"}))
    return response

@blog_manage.route('/blog_top_cancle',methods=['Post',])
def blog_top_cancle():
    '''
    取消置顶
    :return:
    '''
    form = request.form
    blog_opetration_id = form.get('blog_opetration_id')
    connection.update_data(blog_collection,{"_id":ObjectId(blog_opetration_id)},{"$set":{"is_top":False}},multi=True)
    response = get_return_response(jsonify({"status": "success"}))
    return response

@blog_manage.route('/blog_up',methods=['Post',])
def blog_up():
    '''
    博客上架
    :return:
    '''
    form = request.form
    blog_opetration_id = form.get('blog_opetration_id')
    connection.update_data(blog_collection, {"_id": ObjectId(blog_opetration_id)},
                           {"$set": {"is_status": 1}}, multi=True)
    response = get_return_response(jsonify({"status": "success"}))
    return response

@blog_manage.route('/blog_down',methods=['Post',])
def blog_down():
    '''
    博客下架
    :return:
    '''
    form = request.form
    blog_opetration_id = form.get('blog_opetration_id')
    connection.update_data(blog_collection, {"_id": ObjectId(blog_opetration_id)},
                           {"$set": {"is_status": 2}}, multi=True)
    response = get_return_response(jsonify({"status": "success"}))
    return response