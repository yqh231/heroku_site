from blog import app
from blog.blogDB import config_db_session

config_db_session()
app.run(debug=True)