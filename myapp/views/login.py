from flask import Blueprint, request, jsonify, redirect, url_for, render_template

# from forms.login_forms import EmailPasswordForm
from util.post_response import get_return_response
from connect_db.connect_mongo import ConnectMongoDB,ObjectId


login = Blueprint("login", __name__)

connection = ConnectMongoDB()  # 连接数据库
blog_author_collection = connection.get_collection('blog_author')  # 博主信息表

# @login.route('/', methods=["GET", "POST"])
# def to_login():
#     form = EmailPasswordForm()
#     if form.validate_on_submit():
#         # Check the password and log the user in
#         # [...]
#
#         return redirect(url_for('index'))
#     return render_template('login.html', form=form)

@login.route('/')
def to_login():
    return render_template("login.html")


@login.route('/check_login', methods=['POST', ])
def check_login():
    # 验证用户名和密码是否正确
    form = request.form
    username = form.get('username')
    passwd = form.get('passwd')
    results = connection.find_data(blog_author_collection,{'$and':[{'username':username,'passwd':passwd}]})
    flag = results.count() == 1
    # 查询数据库中的用户名密码是否一致
    response = get_return_response(jsonify({"status": flag, "data": {}}))
    return response
