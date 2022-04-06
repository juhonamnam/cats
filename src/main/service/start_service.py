import json
from src.main.model import get_admins, new_user, get_user_info
from src.resources import get_message
from src.main.controller.base import controller


def start_default_service(chat_id, msg_id, first_name, language_code):
    user_info = get_user_info(int(chat_id))

    if user_info != 'NOAUTH':
        return

    inline_keyboard = [
        [{'text': get_message(language_code)(
            'start.request'), 'callback_data': 'subscribe'}]
    ]

    controller.delete_message_thread(chat_id, msg_id)
    controller.send_message_with_dict({
        'chat_id': chat_id,
        'text': get_message(language_code)('start.default').format(name=first_name),
        'reply_markup': json.dumps({
            'inline_keyboard': inline_keyboard
        }),
        'parse_mode': 'HTML'
    })


def subscribe_service(chat_id, msg_id, first_name, language_code, callback_query_id):
    user_info = get_user_info(int(chat_id))

    if user_info != 'NOAUTH':
        language_code = user_info.language
        controller.delete_message_thread(chat_id, msg_id)
        controller.answer_callback_query_with_dict(
            {'callback_query_id': callback_query_id, 'text': get_message(language_code)('start.alr_subscribed')})
        return

    admins = get_admins()

    controller.edit_message_with_dict(
        {'chat_id': chat_id, 'message_id': msg_id, 'text': get_message(language_code)('start.request.sent')})

    controller.send_messages([{
        'chat_id': admin.id,
        'text': get_message(admin.language)('start.requestmess').format(first_name),
        'reply_markup': json.dumps({
            'inline_keyboard': [[{'text': get_message(admin.language)('com.accept'), 'callback_data': f'accept {chat_id} {language_code} {first_name}'},
                                 {'text': get_message(admin.language)('com.reject'), 'callback_data': f'reject {chat_id} {first_name}'}]],
        })
    } for admin in admins])


def subscribe_accept_service(chat_id, msg_id, args, language_code, callback_query_id):
    user_info = get_user_info(chat_id)

    if user_info != 'NOAUTH':
        language_code = user_info.language

    if user_info == 'NOAUTH' or not user_info.is_admin:
        controller.delete_message_thread(chat_id, msg_id)
        controller.answer_callback_query_with_dict(
            {'callback_query_id': callback_query_id, 'text': get_message(language_code)('com.noauth')})
        return

    new_user_chat_id = int(args[0])
    user_language_code = args[1]
    first_name = ' '.join(args[2:])
    new_user_info = get_user_info(new_user_chat_id)
    if new_user_info == 'NOAUTH':

        responsecode = new_user(
            new_user_chat_id, first_name, language=user_language_code)
        if responsecode == '0000':
            controller.delete_message_thread(chat_id, msg_id)
            controller.answer_callback_query_with_dict({
                'callback_query_id': callback_query_id,
                'text': get_message(language_code)('start.request.acceptmess')
                .format(first_name)
            })
            controller.send_message_with_dict({
                'chat_id': new_user_chat_id,
                'text': get_message(user_language_code)('start.request.accept')
            })
        else:
            controller.answer_callback_query_with_dict({
                'callback_query_id': callback_query_id,
                'text': get_message(language_code)('com.failed')
            })

    else:
        controller.delete_message_thread(chat_id, msg_id)
        controller.answer_callback_query_with_dict({
            'callback_query_id': callback_query_id,
            'text': get_message(language_code)('start.alr_subscribedmess')
            .format(first_name)
        })


def reject_service(chat_id, msg_id, args, language_code, callback_query_id):
    user_info = get_user_info(chat_id)

    if user_info != 'NOAUTH':
        language_code = user_info.language

    if user_info == 'NOAUTH' or not user_info.is_admin:
        controller.delete_message_thread(chat_id, msg_id)
        controller.answer_callback_query_with_dict(
            {'callback_query_id': callback_query_id, 'text': get_message(language_code)('com.noauth')})
        return

    first_name = ' '.join(args[1:])

    controller.delete_message_thread(chat_id, msg_id)
    controller.answer_callback_query_with_dict({
        'callback_query_id': callback_query_id,
        'text': get_message(language_code)('start.request.rejectmess')
        .format(first_name)
    })
