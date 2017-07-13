import time
from flask import Flask, Blueprint, request, jsonify, render_template
from flask_login import login_required

from util.post_response import get_return_response

webuploader = Blueprint("webuploader", __name__)

@webuploader.route('/upload',methods=['Post',])
def upload():
    print('请求')
    file = request.files['file']
    path = '/home/hadoop/PycharmProjects/170709/llws_blog_rest/myapp/static/title_imgs/'
    filename = "%s%s"%(time.strftime('%Y%m%d%H%M%S', time.localtime(time.time())),file.filename[file.filename.rindex('.'):])
    file.save(path + filename)
    response = get_return_response(jsonify({"status": True,"data":{"title_img_url":path + filename}}))
    return response