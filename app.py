from flask import Flask
from database import init_db
from routes import api

app = Flask(__name__)
app.register_blueprint(api)

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
