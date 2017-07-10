from flask import Flask, render_template, make_response, redirect, url_for

from views.login import login
from views.index import index

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
    # return redirect(url_for('login.to_login'))
    return render_template("login.html")


def get_return_response(data2return):
    # 获取封装着返回数据的response
    response = make_response(data2return)
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'POST'
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    return response


if __name__ == '__main__':
    app.register_blueprint(login, url_prefix='/login')
    app.register_blueprint(index, url_prefix='/index')
    app.run(host='0.0.0.0', debug=app.config['DEBUG'])
    # app.run(host='0.0.0.0', debug=True)
