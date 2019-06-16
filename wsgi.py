#!/usr/bin/env python

from flask_view_demo import app

# Expose application for gunicorn.
application = app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
