# -*- coding: utf-8 -*-
import os
import re
import json
from flask import Flask, request, render_template, url_for, make_response,Blueprint,jsonify
from uploader import Uploader
from util.post_response import get_return_response

# app = Flask(__name__)
blog_add = Blueprint("blog_add", __name__)

