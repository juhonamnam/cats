import json
from src.main.model import update_user, delete_user, get_user_info
from src.resources import get_message
from src.main.controller.base import controller


def setting_service(chat_id, language_code, msg_id, callback_query_id=None):
    user_info = get_user_info(chat_id)

    if user_info == 'NOAUTH':
        if callback_query_id:
            controller.delete_message_thread(chat_id, msg_id)
            controller.answer_callback_query_with_dict(
                {'callback_query_id': callback_query_id, 'text': get_message(language_code)('com.noauth')})
        return

    language_code = user_info.language

    inline_keyboard = [
        [{'text': get_message(language_code)('setting.activitystate'), 'callback_data': 'activity'},
         {'text': 'Language/언어', 'callback_data': 'language'}],
        [{'text': get_message(language_code)('setting.editname'), 'callback_data': 'edit_name_input'},
         {'text': get_message(language_code)('setting.unsubscribe'), 'callback_data': 'unsubscribe_confirm'}],
        [{'text': get_message(language_code)('com.exit'),
          'callback_data': 'exit'}]
    ]

    if callback_query_id:
        controller.edit_message_with_dict({
            'chat_id': chat_id,
            'message_id': msg_id,
            'text': get_message(language_code)('setting.default').format(name=user_info.name, activity_state=get_message(language_code)('setting.active') if user_info.is_active else get_message(language_code)('setting.inactive')),
            'reply_markup': json.dumps({
                'inline_keyboard': inline_keyboard
            }),
            'parse_mode': 'HTML'
        })

    else:
        controller.delete_message_thread(chat_id, msg_id)
        controller.send_message_with_dict({
            'chat_id': chat_id,
            'text': get_message(language_code)('setting.default').format(name=user_info.name, activity_state=get_message(language_code)('setting.active') if user_info.is_active else get_message(language_code)('setting.inactive')),
            'reply_markup': json.dumps({
                'inline_keyboard': inline_keyboard
            }),
            'parse_mode': 'HTML'
        })


def activity_service(chat_id, msg_id, language_code, callback_query_id):
    user_info = get_user_info(chat_id)

    if user_info == 'NOAUTH':
        controller.delete_message_thread(chat_id, msg_id)
        controller.answer_callback_query_with_dict(
            {'callback_query_id': callback_query_id, 'text': get_message(language_code)('com.noauth')})
        return

    language_code = user_info.language

    if user_info.is_active:
        inline_keyboard = [
            [{'text': get_message(language_code)(
                'setting.deactivate'), 'callback_data': 'set_activity deactivate'},
             {'text': get_message(language_code)('setting.backtosetting'), 'callback_data': 'setting'}],
        ]
        controller.edit_message_with_dict({
            'chat_id': chat_id,
            'message_id': msg_id,
            'text': get_message(language_code)('setting.deactivate.confirm'),
            'reply_markup': json.dumps({
                'inline_keyboard': inline_keyboard
            }),
            'parse_mode': 'HTML'
        })

    else:
        inline_keyboard = [
            [{'text': get_message(language_code)(
                'setting.activate'), 'callback_data': 'set_activity activate'},
             {'text': get_message(language_code)(
                 'setting.backtosetting'), 'callback_data': 'setting'}],
        ]
        controller.edit_message_with_dict({
            'chat_id': chat_id,
            'message_id': msg_id,
            'text': get_message(language_code)('setting.activate.confirm'),
            'reply_markup': json.dumps({
                'inline_keyboard': inline_keyboard
            }),
            'parse_mode': 'HTML'
        })


def set_activity_service(chat_id, msg_id, language_code, activity_status: bool, callback_query_id):
    user_info = get_user_info(chat_id)

    if user_info == 'NOAUTH':
        controller.delete_message_thread(chat_id, msg_id)
        controller.answer_callback_query_with_dict(
            {'callback_query_id': callback_query_id, 'text': get_message(language_code)('com.noauth')})
        return

    language_code = user_info.language

    responsecode = update_user(chat_id, is_active=activity_status)

    if responsecode == '0000':
        controller.delete_message_thread(chat_id, msg_id)
        controller.answer_callback_query_with_dict({
            'callback_query_id': callback_query_id,
            'text': get_message(language_code)('com.success')
        })

    else:
        controller.delete_message_thread(chat_id, msg_id)
        controller.answer_callback_query_with_dict({
            'callback_query_id': callback_query_id,
            'text': get_message(language_code)('com.failed')
        })


def unsubscribe_confirm_service(chat_id, msg_id, language_code, callback_query_id):
    user_info = get_user_info(chat_id)

    if user_info == 'NOAUTH':
        controller.delete_message_thread(chat_id, msg_id)
        controller.answer_callback_query_with_dict(
            {'callback_query_id': callback_query_id, 'text': get_message(language_code)('com.noauth')})
        return

    language_code = user_info.language

    inline_keyboard = [
        [{'text': get_message(language_code)('setting.unsubscribe'), 'callback_data': 'unsubscribe'},
         {'text': get_message(language_code)('setting.backtosetting'), 'callback_data': 'setting'}],
    ]

    controller.edit_message_with_dict({
        'chat_id': chat_id,
        'message_id': msg_id,
        'text': get_message(language_code)('setting.unsubscribe.confirm'),
        'reply_markup': json.dumps({
            'inline_keyboard': inline_keyboard
        })
    })


def unsubscribe_service(chat_id, msg_id, language_code, callback_query_id):
    user_info = get_user_info(chat_id)

    if user_info == 'NOAUTH':
        controller.delete_message_thread(chat_id, msg_id)
        controller.answer_callback_query_with_dict(
            {'callback_query_id': callback_query_id, 'text': get_message(language_code)('com.noauth')})
        return

    language_code = user_info.language

    responescode = delete_user(chat_id)

    if responescode == '0000':
        controller.delete_message_thread(chat_id, msg_id)
        controller.answer_callback_query_with_dict({
            'callback_query_id': callback_query_id,
            'text': get_message(language_code)('com.success')
        })

    else:
        controller.delete_message_thread(chat_id, msg_id)
        controller.answer_callback_query_with_dict({
            'callback_query_id': callback_query_id,
            'text': get_message(language_code)('com.failed')
        })


def language_service(chat_id, msg_id, language_code, callback_query_id):
    user_info = get_user_info(chat_id)

    if user_info == 'NOAUTH':
        controller.delete_message_thread(chat_id, msg_id)
        controller.answer_callback_query_with_dict(
            {'callback_query_id': callback_query_id, 'text': get_message(language_code)('com.noauth')})
        return

    language_code = user_info.language

    inline_keyboard = [
        [{'text': 'English', 'callback_data': 'set_language en'},
         {'text': '한국어', 'callback_data': 'set_language ko'}],
        [{'text': get_message(language_code)(
            'setting.backtosetting'), 'callback_data': 'setting'}]
    ]
    controller.edit_message_with_dict({
        'chat_id': chat_id,
        'message_id': msg_id,
        'text': get_message(language_code)('setting.language.curr'),
        'reply_markup': json.dumps({
            'inline_keyboard': inline_keyboard
        }),
        'parse_mode': 'HTML'
    })


def set_language_service(chat_id, msg_id, language_code, language: str, callback_query_id):
    user_info = get_user_info(chat_id)

    if user_info == 'NOAUTH':
        controller.delete_message_thread(chat_id, msg_id)
        controller.answer_callback_query_with_dict(
            {'callback_query_id': callback_query_id, 'text': get_message(language_code)('com.noauth')})
        return

    responsecode = update_user(chat_id, language=language)

    if responsecode == '0000':
        language_code = language
        controller.delete_message_thread(chat_id, msg_id)
        controller.answer_callback_query_with_dict({
            'callback_query_id': callback_query_id,
            'text': get_message(language_code)('com.success')
        })

    else:
        language_code = user_info.language
        controller.delete_message_thread(chat_id, msg_id)
        controller.answer_callback_query_with_dict({
            'callback_query_id': callback_query_id,
            'text': get_message(language_code)('com.failed')
        })


def edit_name_input_service(chat_id, msg_id, language_code, callback_query_id):
    user_info = get_user_info(chat_id)

    if user_info == 'NOAUTH':
        controller.delete_message_thread(chat_id, msg_id)
        controller.answer_callback_query_with_dict(
            {'callback_query_id': callback_query_id, 'text': get_message(language_code)('com.noauth')})
        return

    language_code = user_info.language

    controller.delete_message_thread(chat_id, msg_id)
    controller.send_message_with_dict({
        'chat_id': chat_id,
        'text': get_message(language_code)('setting.editnameinput'),
        'reply_markup': json.dumps({
            'force_reply': True,
            'input_field_placeholder': get_message(language_code)('setting.editnameinput.placeholder'),
        }),
        'parse_mode': 'HTML'
    })


def edit_name_confirm_service(chat_id, msg_id, reply_msg_id, new_name, language_code):
    user_info = get_user_info(chat_id)

    if user_info == 'NOAUTH':
        controller.delete_message_thread(chat_id, reply_msg_id)
        controller.delete_message_thread(chat_id, msg_id)
        controller.send_message_with_dict(
            {'chat_id': chat_id, 'text': get_message(language_code)('com.noauth')})
        return

    language_code = user_info.language

    inline_keyboard = [
        [{'text': get_message(language_code)('com.yes'), 'callback_data': f'edit_name {new_name}'},
         {'text': get_message(language_code)('com.no'), 'callback_data': 'setting'}],
    ]

    controller.delete_message_thread(chat_id, reply_msg_id)
    controller.delete_message_thread(chat_id, msg_id)
    controller.send_message_with_dict({
        'chat_id': chat_id,
        'text': get_message(language_code)('setting.editname.confirm').format(new_name=new_name),
        'reply_markup': json.dumps({
            'inline_keyboard': inline_keyboard
        }),
        'parse_mode': 'HTML'
    })


def edit_name_service(chat_id, msg_id, language_code, new_name, callback_query_id):
    user_info = get_user_info(chat_id)

    if user_info == 'NOAUTH':
        controller.delete_message_thread(chat_id, msg_id)
        controller.answer_callback_query_with_dict(
            {'callback_query_id': callback_query_id, 'text': get_message(language_code)('com.noauth')})
        return

    language_code = user_info.language

    responsecode = update_user(chat_id, name=new_name)

    if responsecode == '0000':
        controller.delete_message_thread(chat_id, msg_id)
        controller.answer_callback_query_with_dict({
            'callback_query_id': callback_query_id,
            'text': get_message(language_code)('com.success')
        })

    else:
        controller.delete_message_thread(chat_id, msg_id)
        controller.answer_callback_query_with_dict({
            'callback_query_id': callback_query_id,
            'text': get_message(language_code)('com.failed')
        })
