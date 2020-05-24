from . import app

if __name__ == '__main__':
    settings = dict(
        host='0.0.0.0',
        port=5000,
        debug=False,
        use_reloader=False,
    )
    app.run(**settings)
