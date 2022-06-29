from env import api_key, is_production
from src.telesk import Telesk
from src.main.controller import controller
from src.resources import get_commands
import logging.config
import json
import os

if is_production:
    if not os.path.exists('./logs'):
        os.mkdir('./logs')
    logging.config.dictConfig(json.load(open('./logger.main.json')))
else:
    logging.config.dictConfig(json.load(open('./logger.dev.json')))

app = Telesk()
app.config['api_key'] = api_key
app.config['commands'] = get_commands()
app.config['allow_group'] = False
app.register_blueprint(controller)

if __name__ == '__main__':
    app.poll()
