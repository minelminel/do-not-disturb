from . import app

if __name__ == '__main__':
    settings = dict(
        host='0.0.0.0',
        port=5000,
        debug=True,
        use_reloader=True,
    )
    app.run(**settings)
