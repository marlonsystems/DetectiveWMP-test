from flask import Flask, render_template
from database import init_db
from routes import api

app = Flask(__name__)
app.register_blueprint(api)

@app.route("/")
def dashboard():
    return render_template("index.html")

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
