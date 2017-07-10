from myapp import *

app.register_blueprint(login, url_prefix='/login')
app.register_blueprint(index, url_prefix='/index')
app.run(host='0.0.0.0', debug=app.config['DEBUG'])
