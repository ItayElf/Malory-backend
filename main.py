from flask import Flask
from settings import VERSION

app = Flask(__name__)

# imports all api endpoints
from endpoints.api import *
from endpoints.actions import *


if __name__ == '__main__':
    app.run()
