import os
import sys
from src.telesk import Telesk
from src.websocket.upbit_websocket import UpbitWebsocket
from src.main.controller.base import controller
import logging.config
import json

if len(sys.argv) > 1 and sys.argv[1] == 'dev':
    logging.config.dictConfig(json.load(open('./logger.ws.dev.json')))
else:
    logging.config.dictConfig(json.load(open('./logger.local.json')))

telesk_app = Telesk()
telesk_app.config['api_key'] = os.getenv('CATS_TELE_KEY')
telesk_app.register_blueprint(controller)

ws = UpbitWebsocket(
    ['KRW-BTC', 'KRW-ETH', 'KRW-EOS', 'KRW-BCH'])

if __name__ == '__main__':
    ws.run()
