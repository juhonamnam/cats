from .base import controller
from src.main import service


@controller.route('/about')
def setting_command(chat_id, args, msg_info):
    language_code = msg_info['from']['language_code']
    msg_id = msg_info['message_id']
    service.about_service(chat_id, language_code, msg_id)


@controller.route('exit', type='callback')
def setting_command(chat_id, msg_id, args, callback_info):
    controller.delete_message(chat_id, msg_id)


@controller.route('dummy_callback', type='callback')
def setting_command(chat_id, msg_id, args, callback_info):
    controller.answer_callback_query(
        callback_info['id'], cache_time=10000)


@controller.route('/')
def edit_name_command(chat_id, text, msg_info):
    reply = msg_info.get('reply_to_message')
    if reply and reply['text'] in ['Enter new name']:
        language_code = msg_info['from']['language_code']
        msg_id = msg_info['message_id']
        reply_msg_id = reply['message_id']
        service.edit_name_confirm_service(
            chat_id, msg_id, reply_msg_id, text, language_code)
