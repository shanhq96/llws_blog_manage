from flask import Flask, redirect, render_template

from views.login import login
from views.index import index
from views.blog_manage import blog_manage
from views.comment_mange import comment_manage
from util.ueditor_server import ueditor_server
# [...] Initialize the app
from flask_login import login_required, current_user

app = Flask(__name__, instance_relative_config=True)
from util.util import ListConverter

app.url_map.converters['list'] = ListConverter

app.config.from_object('config.default')
app.config.from_pyfile('config.py')  # 从instance文件夹中加载配置


# app.config.from_envvar(‘APP_CONFIG_FILE’)将加载由环境变量APP_CONFIG_FILE指定的文件。这个环境变量的值应该是一个配置文件的绝对路径。
# APP_CONFIG_FILE=/var/www/yourapp/config/production.py
# python llws_blog_manage.py
# app.config.from_envvar('APP_CONFIG_FILE')


@app.route('/')
def to_login():
    return redirect('login')
    # return render_template("login.html")


@app.errorhandler(404)
def page_not_found(e):
    """
    url错误,去404页面
    :param e:
    :return:
    """
    return redirect('404'), 404


@app.route('/404')
def to_404():
    """
    去404页面
    :return:
    """
    return render_template('404.html'), 404


def run():
    app.register_blueprint(login, url_prefix='/login')
    app.register_blueprint(index, url_prefix='/index')
    app.register_blueprint(blog_manage, url_prefix='/blog_manage')
    app.register_blueprint(comment_manage, url_prefix='/comment_manage')
    app.register_blueprint(ueditor_server, url_prefix='/ueditor_server')
    app.run(host='0.0.0.0', debug=app.config['DEBUG'])


if __name__ == '__main__':
    run()
    # app.run(host='0.0.0.0', debug=True)
