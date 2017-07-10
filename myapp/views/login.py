from flask import Blueprint, request, jsonify, redirect, url_for, render_template

# from forms.login_forms import EmailPasswordForm

login = Blueprint("login", __name__)


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
    flag = username == "shq" and passwd == "123456"
    # 查询数据库中的用户名密码是否一致
    from llws_blog_manage import get_return_response
    response = get_return_response(
        jsonify({"status": flag, "data": {"username": username}}))
    return response
