from env import api_key, is_production
from src.telesk import Telesk
from src.websocket.upbit_websocket import UpbitWebsocket
from src.main.controller.base import controller
import logging.config
import json
import signal

def handle_sigterm(*args):
    raise KeyboardInterrupt()

signal.signal(signal.SIGTERM, handle_sigterm)

if is_production:
    logging.config.dictConfig(json.load(open('./logger.ws.json')))
else:
    logging.config.dictConfig(json.load(open('./logger.dev.json')))

telesk_app = Telesk()
telesk_app.config['api_key'] = api_key
telesk_app.register_blueprint(controller)

ws = UpbitWebsocket(
    ['KRW-BTC', 'KRW-ETH', 'KRW-EOS', 'KRW-BCH'])

if __name__ == '__main__':
    ws.run()
