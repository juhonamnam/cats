from .base import controller
from src.main import service


@controller.route('/setting')
def setting_command(chat_id, args, msg_info):
    language_code = msg_info['from']['language_code']
    msg_id = msg_info['message_id']
    service.setting_service(chat_id, language_code, msg_id)


@controller.route('setting', type='callback')
def setting_command(chat_id, msg_id, args, callback_info):
    callback_query_id = callback_info['id']
    language_code = callback_info['from']['language_code']
    service.setting_service(chat_id, language_code, msg_id,
                            callback_query_id=callback_query_id)


@controller.route('activity', type='callback')
def activity_callback(chat_id, msg_id, args, callback_info):
    callback_query_id = callback_info['id']
    language_code = callback_info['from']['language_code']
    service.activity_service(chat_id, msg_id, language_code, callback_query_id)


@controller.route('set_activity', type='callback')
def activate_callback(chat_id, msg_id, args, callback_info):
    callback_query_id = callback_info['id']
    language_code = callback_info['from']['language_code']
    if args[0] == 'activate':
        activity_status = True
    else:
        activity_status = False
    service.set_activity_service(
        chat_id, msg_id, language_code, activity_status, callback_query_id)


@controller.route('unsubscribe_confirm', type='callback')
def unsubscribe_callback(chat_id, msg_id, args, callback_info):
    callback_query_id = callback_info['id']
    language_code = callback_info['from']['language_code']
    service.unsubscribe_confirm_service(
        chat_id, msg_id, language_code, callback_query_id)


@controller.route('unsubscribe', type='callback')
def unsubscribe_callback(chat_id, msg_id, args, callback_info):
    callback_query_id = callback_info['id']
    language_code = callback_info['from']['language_code']
    service.unsubscribe_service(
        chat_id, msg_id, language_code, callback_query_id)


@controller.route('language', type='callback')
def activity_callback(chat_id, msg_id, args, callback_info):
    callback_query_id = callback_info['id']
    language_code = callback_info['from']['language_code']
    service.language_service(chat_id, msg_id, language_code, callback_query_id)


@controller.route('set_language', type='callback')
def activate_callback(chat_id, msg_id, args, callback_info):
    callback_query_id = callback_info['id']
    language_code = callback_info['from']['language_code']
    language = args[0]
    service.set_language_service(
        chat_id, msg_id, language_code, language, callback_query_id)


@controller.route('edit_name_input', type='callback')
def edit_name_input_callback(chat_id, msg_id, args, callback_info):
    callback_query_id = callback_info['id']
    language_code = callback_info['from']['language_code']
    service.edit_name_input_service(
        chat_id, msg_id, language_code, callback_query_id)


@controller.route('edit_name', type='callback')
def edit_name_callback(chat_id, msg_id, args, callback_info):
    callback_query_id = callback_info['id']
    new_name = ' '.join(args)
    language_code = callback_info['from']['language_code']
    service.edit_name_service(
        chat_id, msg_id, language_code, new_name, callback_query_id)
