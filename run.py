"""
This code runs the dash setup for hosting the web-app
"""
from app.app import app

server = app.server

if __name__ == '__main__':
    app.run_server(debug=True)
