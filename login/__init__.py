from flask import Flask, Blueprint, request,jsonify
import llws_blog_manage

login = Blueprint("login", __name__)


@login.route('/check_login', methods=['POST', ])
def check_login():
    # 验证用户名和密码是否正确
    form = request.form
    username = form.get('username')
    passwd = form.get('passwd')
    flag = username == "shq" and passwd == "123456"
    # 查询数据库中的用户名密码是否一致
    response = llws_blog_manage.get_return_response(
        jsonify({"status": flag, "data": {"username": username}}))
    return response


def __getblueprint__():
    return login
