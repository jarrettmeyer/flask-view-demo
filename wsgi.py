from flask_view_demo import app

# Expose application for gunicorn.
application = app

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
