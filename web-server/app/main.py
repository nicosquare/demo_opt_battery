from app import app
# from app.src.sqlite import db_exists

# sqlite = app.config["DATABASE_URI"]


@app.errorhandler(404)
def not_found(e):
    return '404 not found'
    # return app.send_static_file('index.html')

@app.route('/')
def index():
    return 'running server'
    # return app.send_static_file('index.html')

# def database_init():
#     print('ver url: ', sqlite)
# db_exists(sqlite)
