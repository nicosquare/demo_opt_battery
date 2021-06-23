from app import app

@app.errorhandler(404)
def not_found(e):
    return '404 not found'
    # return app.send_static_file('index.html')

@app.route('/')
def index():
    return 'running server'
    # return app.send_static_file('index.html')
