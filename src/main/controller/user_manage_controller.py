from .base import controller
from src.main import service


@controller.route('/user_manage')
def user_manage_command(chat_id, arg, msg_info):
    language_code = msg_info['from']['language_code']
    msg_id = msg_info['message_id']
    service.user_manage_page_service(chat_id, msg_id, language_code, 0)


@controller.route('user_manage_page', type='callback')
def user_manage_page_callback(chat_id, msg_id, args, callback_info):
    page = int(args[0])
    callback_query_id = callback_info['id']
    language_code = callback_info['from']['language_code']
    service.user_manage_page_service(
        chat_id, msg_id, language_code, page, callback_query_id)


@controller.route('user_manage', type='callback')
def user_manage_callback(chat_id, msg_id, args, callback_info):
    callback_query_id = callback_info['id']
    user_chat_id = int(args[0])
    language_code = callback_info['from']['language_code']
    service.user_manage_service(
        chat_id, user_chat_id, msg_id, language_code, callback_query_id)


@controller.route('promote_confirm', type='callback')
def promote_confirm_callback(chat_id, msg_id, args, callback_info):
    callback_query_id = callback_info['id']
    user_chat_id = int(args[0])
    language_code = callback_info['from']['language_code']
    service.promote_confirm_service(
        chat_id, user_chat_id, msg_id, language_code, callback_query_id)


@controller.route('promote', type='callback')
def promote_callback(chat_id, msg_id, args, callback_info):
    callback_query_id = callback_info['id']
    user_chat_id = int(args[0])
    language_code = callback_info['from']['language_code']
    service.promote_service(chat_id, user_chat_id, msg_id,
                            language_code, callback_query_id)


@controller.route('suspend_confirm', type='callback')
def suspend_confirm_callback(chat_id, msg_id, args, callback_info):
    callback_query_id = callback_info['id']
    user_chat_id = int(args[0])
    language_code = callback_info['from']['language_code']
    service.suspend_confirm_service(
        chat_id, user_chat_id, msg_id, language_code, callback_query_id)


@controller.route('suspend', type='callback')
def suspend_confirm_callback(chat_id, msg_id, args, callback_info):
    callback_query_id = callback_info['id']
    susp_type = args[0]
    user_chat_id = int(args[1])
    language_code = callback_info['from']['language_code']
    service.suspend_service(chat_id, user_chat_id, msg_id,
                            language_code, callback_query_id)
