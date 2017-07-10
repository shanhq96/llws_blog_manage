from flask_assets import Bundle, Environment
from myapp import app

bundles = {

    '_footer_js': Bundle(
        'static/h-ui.admin/lib/jquery/1.9.1/jquery.min.js',
        'static/h-ui.admin/lib/layer/2.4/layer.js',
        'static/h-ui.admin/static/h-ui/js/H-ui.min.js',
        'static/h-ui.admin/static/h-ui.admin/js/H-ui.admin.js',
        output='gen/home.js'),

    'home_css': Bundle(
        'css/lib/reset.css',
        'css/common.css',
        'css/home.css',
        output='gen/home.css'),

    'admin_js': Bundle(
        'js/lib/jquery-1.10.2.js',
        'js/lib/Chart.js',
        'js/admin.js',
        output='gen/admin.js'),

    'admin_css': Bundle(
        'css/lib/reset.css',
        'css/common.css',
        'css/admin.css',
        output='gen/admin.css')
}

assets = Environment(app)

assets.register(bundles)
