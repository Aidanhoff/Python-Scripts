from flask import Flask
app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template(
        "homepage.html"
    )

@app.route('/map/')
def map_page():
    return