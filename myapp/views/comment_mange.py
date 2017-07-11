from flask import Flask,Blueprint,request,jsonify,render_template
from util.post_response import get_return_response

comment_manage = Blueprint("comment_manage", __name__)


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
    test_totle_data_num = 75

    form = request.form
    print(form)
    data_start = int(form.get('start'))
    data_length = int(form.get('length'))
    currentPage = data_start / data_length + 1
    draw = int(form.get('draw'))

    # 构造datatables插件需要的配置数据
    response_datatables = {}
    response_datatables['draw'] = draw
    response_datatables['recordsFiltered'] = test_totle_data_num
    response_datatables['recordsTotal'] = test_totle_data_num

    # 构造返回的data
    response_data_array = []
    for i in range(test_totle_data_num):
        response_data = {}
        response_data['id'] = i
        response_data['user_id'] = 1
        response_data['article_id'] = 1
        response_data['create_time'] = 1
        response_data['content'] = 1
        response_data['response'] = 1
        response_data_array.append(response_data)

    response_datatables['data'] = response_data_array
    print(response_datatables)
    response = get_return_response(jsonify(response_datatables))
    return response
