from flask import Flask

app = Flask(__name__)
VERSION = "0.0.0.1"  # 4.12.21


@app.route("/api/version/")
def version_api():
    return VERSION


if __name__ == '__main__':
    app.run()
