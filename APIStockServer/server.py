from flask import Flask

from alerts import MetalEtfAlerts

app = Flask(__name__)


if __name__ == "__main__":
    app.run()
