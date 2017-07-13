import time
import uuid
import os

from flask import Flask, Blueprint, request, jsonify, render_template
from flask_login import login_required

from util.post_response import get_return_response

webuploader = Blueprint("webuploader", __name__)

@webuploader.route('/upload',methods=['Post',])
def upload():
    file = request.files['file']

    path_head = '/home/hadoop/PycharmProjects/170709/llws_blog_rest/myapp'
    path_tail = '/static/title_imgs/'+time.strftime('%Y%m%d', time.localtime(time.time()))+"/"
    path_total = path_head+path_tail
    if(not os.path.isdir(path_total)):
        os.mkdir(path_total)
    filename_head = time.strftime('%H%M%S', time.localtime(time.time())) + str(uuid.uuid1()).replace('-','')
    filename = "%s%s"%(filename_head,file.filename[file.filename.rindex('.'):])
    file.save(path_total + filename)
    response = get_return_response(jsonify({"status": True,"data":{"title_img_url":path_tail + filename}}))
    return response