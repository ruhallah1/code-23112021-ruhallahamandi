import logging
import os
import config
import json
from apis import api
from flask import Flask, jsonify, request
import requests

logging.basicConfig(level=logging.DEBUG,
                    format='[%(asctime)s]: {} %(levelname)s %(message)s'.format(os.getpid()),
                    datefmt='%Y-%m-%d %H:%M:%S',
                    handlers=[logging.StreamHandler()])

logger = logging.getLogger()


def create_app():
    logger.info('Starting app in {config.APP_ENV} environment')
    app = Flask(__name__)
    app.config.from_object('config')
    api.init_app(app)

    @app.route('/')
    def test():
        return 'Running'


    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host='0.0.0.0', port=5004, debug=False)
