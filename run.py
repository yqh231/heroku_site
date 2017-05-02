from blog import app
from blog.blogDB import config_db_session
from werkzeug.contrib.fixers import ProxyFix
config_db_session()
# app.wsgi_app = ProxyFix(app.wsgi_app)
app.run()