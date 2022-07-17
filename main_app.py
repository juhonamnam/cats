from env import api_key, is_production, sql_url
from src.telesk import Telesk
from src.main.controller import controller
from src.resources import get_commands
from src.main.model.base import db
import logging.config
import json
import signal


def handle_sigterm(*args):
    raise KeyboardInterrupt()


signal.signal(signal.SIGTERM, handle_sigterm)

if is_production:
    logging.config.dictConfig(json.load(open('./logger.main.json')))
else:
    logging.config.dictConfig(json.load(open('./logger.dev.json')))

app = Telesk()
app.config['api_key'] = api_key
app.config['commands'] = get_commands()
app.config['allow_group'] = False
app.register_blueprint(controller)

if __name__ == '__main__':
    db.open(sql_url)
    app.poll(on_disconnect=db.close)
