import time
from flask import Flask, Blueprint, request, jsonify, render_template
from flask_login import login_required

from util.post_response import get_return_response

webuploader = Blueprint("webuploader", __name__)

@webuploader.route('/upload',methods=['Post',])
def upload():
    file = request.files['file']
    path_head = '/home/hadoop/PycharmProjects/170709/llws_blog_rest/myapp'
    path_tail = '/static/title_imgs/'
    filename = "%s%s"%(time.strftime('%Y%m%d%H%M%S', time.localtime(time.time())),file.filename[file.filename.rindex('.'):])
    file.save(path_head + path_tail + filename)
    response = get_return_response(jsonify({"status": True,"data":{"title_img_url":path_tail + filename}}))
    return response