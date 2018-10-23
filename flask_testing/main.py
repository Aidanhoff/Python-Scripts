from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template(
        "main.html"
    )

@app.route('/map/')
def map_page():
    return

if __name__ == '__main__':
    app.run(host='0.0.0.0')