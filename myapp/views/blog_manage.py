from flask import Flask, Blueprint, request, jsonify, render_template

blog_manage = Blueprint("blog_manage", __name__)


@blog_manage.route('/to_blog_manage')
def to_blog_manage():
    return render_template("blog_manage/blog-manage-list.html")