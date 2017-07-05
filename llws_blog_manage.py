from flask import *

import login

app = Flask(__name__)


@app.route('/')
def to_login():
    return render_template("login.html")

@app.route('/index')
def to_index():
    return render_template("index.html")


def get_return_response(data2return):
    # 获取封装着返回数据的response
    response = make_response(data2return)
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'POST'
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    return response


if __name__ == '__main__':
    app.register_blueprint(login.__getblueprint__(), url_prefix='/login')
    app.run(host='0.0.0.0')
