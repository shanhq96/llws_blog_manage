from flask import Flask, Blueprint, request, jsonify, render_template,make_response
# from ueditor import UEditor
from util.post_response import get_return_response
# mongodb数据库连接
from connect_db.connect_mongo import ObjectId, ConnectMongoDB

from uploader import Uploader
from util.post_response import get_return_response
import os
import re
import json
import time

blog_manage = Blueprint("blog_manage", __name__)
# app = Flask(__name__)
# ue = UEditor(app)

connection = ConnectMongoDB()  # 连接数据库
blog_collection = connection.get_collection('blog')

@blog_manage.route('/to_blog_add')
def to_blog_add():
    return render_template("blog_manage/article-add.html")

@blog_manage.route('/upload/', methods=['GET', 'POST', 'OPTIONS'])
def upload():
    """UEditor文件上传接口
    config 配置文件
    result 返回结果
    """
    mimetype = 'application/json'
    result = {}
    action = request.args.get('action')
    # 解析JSON格式的配置文件
    with open(os.path.join(blog_manage.static_folder, 'ueditor', 'php',
                           'config.json')) as fp:
        try:
            # 删除 `/**/` 之间的注释
            CONFIG = json.loads(re.sub(r'\/\*.*\*\/', '', fp.read()))
        except:
            CONFIG = {}
    if action == 'config':
        # 初始化时，返回配置文件给客户端
        result = CONFIG
    elif action in ('uploadimage', 'uploadfile', 'uploadvideo'):
        # 图片、文件、视频上传
        if action == 'uploadimage':
            fieldName = CONFIG.get('imageFieldName')
            config = {
                "pathFormat": CONFIG['imagePathFormat'],
                "maxSize": CONFIG['imageMaxSize'],
                "allowFiles": CONFIG['imageAllowFiles']
            }
        elif action == 'uploadvideo':
            fieldName = CONFIG.get('videoFieldName')
            config = {
                "pathFormat": CONFIG['videoPathFormat'],
                "maxSize": CONFIG['videoMaxSize'],
                "allowFiles": CONFIG['videoAllowFiles']
            }
        else:
            fieldName = CONFIG.get('fileFieldName')
            config = {
                "pathFormat": CONFIG['filePathFormat'],
                "maxSize": CONFIG['fileMaxSize'],
                "allowFiles": CONFIG['fileAllowFiles']
            }
        if fieldName in request.files:
            field = request.files[fieldName]
            uploader = Uploader(field, config, blog_manage.static_folder)
            result = uploader.getFileInfo()
        else:
            result['state'] = '上传接口出错'
    elif action in ('uploadscrawl'):
        # 涂鸦上传
        fieldName = CONFIG.get('scrawlFieldName')
        config = {
            "pathFormat": CONFIG.get('scrawlPathFormat'),
            "maxSize": CONFIG.get('scrawlMaxSize'),
            "allowFiles": CONFIG.get('scrawlAllowFiles'),
            "oriName": "scrawl.png"
        }
        if fieldName in request.form:
            field = request.form[fieldName]
            uploader = Uploader(field, config, blog_manage.static_folder, 'base64')
            result = uploader.getFileInfo()
        else:
            result['state'] = '上传接口出错'
    elif action in ('catchimage'):
        config = {
            "pathFormat": CONFIG['catcherPathFormat'],
            "maxSize": CONFIG['catcherMaxSize'],
            "allowFiles": CONFIG['catcherAllowFiles'],
            "oriName": "remote.png"
        }
        fieldName = CONFIG['catcherFieldName']
        if fieldName in request.form:
            # 这里比较奇怪，远程抓图提交的表单名称不是这个
            source = []
        elif '%s[]' % fieldName in request.form:
            # 而是这个
            source = request.form.getlist('%s[]' % fieldName)
        _list = []
        for imgurl in source:
            uploader = Uploader(imgurl, config, blog_manage.static_folder, 'remote')
            info = uploader.getFileInfo()
            _list.append({
                'state': info['state'],
                'url': info['url'],
                'original': info['original'],
                'source': imgurl,
            })
        result['state'] = 'SUCCESS' if len(_list) > 0 else 'ERROR'
        result['list'] = _list
    else:
        result['state'] = '请求地址出错'
    result = json.dumps(result)
    if 'callback' in request.args:
        callback = request.args.get('callback')
        if re.match(r'^[\w_]+$', callback):
            result = '%s(%s)' % (callback, result)
            mimetype = 'application/javascript'
        else:
            result = json.dumps({'state': 'callback参数不合法'})
    res = make_response(result)
    res.mimetype = mimetype
    res.headers['Access-Control-Allow-Origin'] = '*'
    res.headers['Access-Control-Allow-Headers'] = 'X-Requested-With,X_Requested_With'
    return res



@blog_manage.route('/save_blog', methods=['POST','GET' ])
def save_blog():

    # 验证用户名和密码是否正确
    form = request.form
    print("请让我看到你！！！！！")
    title = form.get('title')
    onetype = form.get('onetype')
    twotype = form.get('twotype')
    maincontent = form.get('maincontent')
    content = form.get('content')
    info = {}
    info['title'] = title  # 标题
    info['big_label'] = onetype  # 一级分类
    info['small_label'] = twotype  # 二级分类
    info['content'] = content  # 内容
    info['describe'] = maincontent  # 概要
    info['is_status'] = 0  # 0未发布
    info['create_time'] = time.time()#创建时间
    info['title_img_url'] = ''#标题图片
    info['hits'] = 0#点击次数
    info['is_top'] = 'false'#是否置顶
    print(info['create_time'], info['title'])
    connection.insert_list(blog_collection,info)

    response = get_return_response(jsonify({"status": 1}))
    return response
    # username = form.get('username')
    # passwd = form.get('passwd')
    # flag = username == "shq" and passwd == "123456"
    # return render_template("welcome/welcome.html")
    # if request.form["action"] == "saveandsubmit":
    #     return render_template("welcome/welcome.html")
    # elif request.form["action"] == "saveonly":
    #     return render_template("blog_manage/blog-manage-list.html")




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
    test_totle_data_num = 75

    form = request.form
    print(form)
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
    ii = data_start
    response_data_array = []
    for response_data in result:
        ii += 1
        response_data['_id'] = str(response_data['_id'])
        # response_data = {}
        # response_data['id'] = i
        response_data['title'] = ii
        response_data['describe'] = ii
        response_data['big_label'] = ii
        response_data['small_label'] = ii
        response_data['url'] = ii
        response_data['create_time'] = ii
        response_data['update_time'] = ii
        response_data['hits'] = ii
        response_data['is_top'] = ii<4
        response_data['is_status'] = 1
        response_data_array.append(response_data)

    response_datatables['data'] = response_data_array
    print(response_datatables)
    response = get_return_response(jsonify(response_datatables))
    return response