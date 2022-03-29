import os
import sys
from src.telesk import Telesk
from src.websocket.upbit_websocket import UpbitWebsocket
import logging.config
import json

if len(sys.argv) > 1 and sys.argv[1] == 'dev':
    logging.config.dictConfig(json.load(open('./logger.ws.dev.json')))
else:
    logging.config.dictConfig(json.load(open('./logger.local.json')))

app = Telesk()
app.config['api_key'] = os.getenv('tele_key')
ws = UpbitWebsocket(
    ['KRW-BTC', 'KRW-ETH', 'KRW-EOS', 'KRW-BCH'], telesk_app=app)

if __name__ == '__main__':
    ws.run()
