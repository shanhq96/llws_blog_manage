from flask import Flask, Blueprint, request, jsonify, render_template
from flask_login import login_required

from util.post_response import get_return_response

webuploader = Blueprint("webuploader", __name__)

@webuploader.route('/upload',methods=['Post',])
def upload():
    print('请求')
    file = request.files['file']
    


    response = get_return_response(jsonify({"status": True}))
    return response