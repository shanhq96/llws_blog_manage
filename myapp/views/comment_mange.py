import time

from flask import Flask, Blueprint, request, jsonify, render_template

# mongodb数据库连接
from connect_db.connect_mongo import ConnectMongoDB, ObjectId
from util.post_response import get_return_response

comment_manage = Blueprint("comment_manage", __name__)

connection = ConnectMongoDB()  # 连接数据库
comment_collection = connection.get_collection('comment')  # 博客表


@comment_manage.route('/to_comment_manage')
def to_comment_manage():
    """去评论列表页
    :return: 评论列表页模版
    """
    return render_template("comment_manage/comment-manage-list.html")


@comment_manage.route('/get_commit_manage_list', methods=['Post', 'Get'])
def get_commit_list():
    """
    获取评论列表页的datatable
    :return:
    """
    form = request.form
    print(form)
    data_start = int(form.get('start'))
    data_length = int(form.get('length'))
    currentPage = data_start / data_length + 1
    draw = int(form.get('draw'))

    # 查询数据库
    result_temp = connection.find_data(comment_collection, {"$and": [{"is_del": 0}]})
    result = result_temp.skip(data_start).limit(data_length)

    # 构造datatables插件需要的配置数据
    response_datatables = {}
    response_datatables['draw'] = draw
    response_datatables['recordsFiltered'] = result_temp.count()
    response_datatables['recordsTotal'] = result_temp.count()

    # 构造返回的data
    response_data_array = []
    for response_data in result:
        response_data['_id'] = str(response_data['_id'])
        response_data['user_id'] = str(response_data['user_id'])
        response_data['blog_id'] = str(response_data['blog_id'])
        response_data_array.append(response_data)

    response_datatables['data'] = response_data_array
    print(response_datatables)
    response = get_return_response(jsonify(response_datatables))
    return response


@comment_manage.route('/delete_comment', methods=['Post'])
def delete_comment():
    """
    删除评论
    :return:
    """
    form = request.form
    comment_to_del_id = form.get('comment_to_del_id')
    connection.update_data(comment_collection, {"_id": ObjectId(comment_to_del_id)}, {"$set": {"is_del": 1}},
                           multi=True)
    response = get_return_response(jsonify({"status": "success"}))
    return response


@comment_manage.route('/reply_comment/<id>', methods=['Get'])
def reply_comment(id):
    """
    回复评论页面
    :return:
    """
    # print(id)
    return render_template("comment_manage/comment-manage-reply.html", var1=id)


@comment_manage.route('/reply_comment_submit', methods=['Post'])
def reply_comment_submit():
    """
    回复评论提交
    :return:
    """
    form = request.form
    id = form.get('id')
    reply = form.get('label_name')
    print(id)
    print(reply)
    connection.update_data(comment_collection, {"_id": ObjectId(id)}, {"$set": {"response": reply}}, multi=True)
    response = get_return_response(jsonify({"status": "success"}))
    return response
