from flask import Flask
from visualization.result import result
from visualization.analyze import analyze

app = Flask(__name__)

if __name__ == '__main__':
    app.register_blueprint(result)
    app.register_blueprint(analyze)
    app.run(debug=True)
