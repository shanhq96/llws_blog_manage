from flask import Flask, Blueprint, request, jsonify, render_template
from flask_login import login_required

index = Blueprint("index", __name__)


@index.route('/')
# @login_required
def to_index():
    return render_template("index.html")
