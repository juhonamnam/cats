from .base import controller
from src.main import service


@controller.route('/start')
def start_command(chat_id, args, msg_info):
    first_name = msg_info['from']['first_name']
    language_code = msg_info['from']['language_code']
    msg_id = msg_info['message_id']
    service.start_default_service(chat_id, msg_id, first_name, language_code)


@controller.route('subscribe', type='callback')
def subscribe_callback(chat_id, msg_id, args, callback_info):
    callback_query_id = callback_info['id']
    first_name = callback_info['from']['first_name']
    language_code = callback_info['from']['language_code']
    service.subscribe_service(
        chat_id, msg_id, first_name, language_code, callback_query_id)


@controller.route('accept', type='callback')
def accept_callback(chat_id, msg_id, args, callback_info):
    callback_query_id = callback_info['id']
    language_code = callback_info['from']['language_code']
    service.subscribe_accept_service(
        chat_id, msg_id, args, language_code, callback_query_id)
