from flask import Flask
from .lnurl_handler import lnurl_routes

app = Flask(__name__)

# Register LNURL Blueprint
app.register_blueprint(lnurl_routes)

# Serve static files from the 'static' folder
app.static_folder = 'static'

# Example route to serve a static HTML file
@app.route('/example')
def example():
    return app.send_static_file('example.html')
