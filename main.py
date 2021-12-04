from flask import Flask
from settings import VERSION

app = Flask(__name__)


@app.route("/api/version/")
def version_api():
    return VERSION


if __name__ == '__main__':
    app.run()
