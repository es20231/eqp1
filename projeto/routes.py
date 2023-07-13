from projeto import app
from projeto import db

@app.route('/')
def page_home():
    return 'HelloWorld'