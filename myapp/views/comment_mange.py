from flask import Flask,Blueprint,request,jsonify,render_template

comment_manage = Blueprint("comment_manage", __name__)


@comment_manage.route('/to_comment_manage')
def to_comment_manage():
    return render_template("comment_manage/comment-manage-list.html")