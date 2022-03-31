import json
from src.main.model import delete_user, update_user, get_users_list, get_user_info
from src.resources import get_message
from src.main.controller.base import controller


def user_manage_page_service(chat_id, msg_id, language_code, page, callback_query_id=None, limit=8, row=4):
    user_info = get_user_info(chat_id)

    if user_info != 'NOAUTH':
        language_code = user_info.language

    if user_info == 'NOAUTH' or not user_info.is_admin:
        if callback_query_id:
            controller.delete_message_thread(chat_id, msg_id)
            controller.answer_callback_query_with_dict(
                {'callback_query_id': callback_query_id, 'text': get_message(language_code)('com.noauth')})
        return

    users = get_users_list(page, limit)

    total = users["paginate"]["total"]

    text = get_message(language_code)(
        'usermanage.page').format(total, page + 1)

    inline_keyboard = []

    user_list = users['list']

    for i in range(limit-len(user_list)):
        user_list.append(None)

    col = int(limit / row)

    for i in range(row):
        row = list()
        for user in user_list[i * col:i * col + col]:
            if user:
                name = user.name
                if user.is_admin:
                    name = name + '(admin)'
                row.append(
                    {'text': name, 'callback_data': f'user_manage {user.id}'})
            else:
                row.append({'text': ' ', 'callback_data': f'dummy_callback'})

        inline_keyboard.append(row)

    max_page = (total - 1) // limit
    if max_page > 0 or page != 0:
        pager_link = list()
        block_page = page // 5

        if block_page != 0:
            pager_link.append(
                {'text': '<<', 'callback_data': 'user_manage_page 0'})
            pager_link.append(
                {'text': '<', 'callback_data': f'user_manage_page {(block_page) * 5 - 1}'})

        for _page in range(block_page * 5, min(block_page * 5 + 5, max_page + 1)):
            if _page == page:
                pager_link.append(
                    {'text': f'({_page + 1})', 'callback_data': f'user_manage_page {_page}'})
            else:
                pager_link.append(
                    {'text': f'{_page + 1}', 'callback_data': f'user_manage_page {_page}'})

        if block_page != max_page // 5:
            pager_link.append(
                {'text': '>', 'callback_data': f'user_manage_page {(block_page) * 5 + 5}'})
            pager_link.append(
                {'text': '>>', 'callback_data': f'user_manage_page {max_page}'})

        inline_keyboard.append(pager_link)
    inline_keyboard.append(
        [{'text': get_message(language_code)('com.exit'), 'callback_data': 'exit'}])

    if callback_query_id:
        controller.edit_message_with_dict({
            'chat_id': chat_id,
            'message_id': msg_id,
            'text': text,
            'reply_markup': json.dumps({
                'inline_keyboard': inline_keyboard
            }),
            'parse_mode': 'HTML'
        })

    else:
        controller.delete_message_thread(chat_id, msg_id)
        controller.send_message_with_dict({
            'chat_id': chat_id,
            'text': text,
            'reply_markup': json.dumps({
                'inline_keyboard': inline_keyboard
            }),
            'parse_mode': 'HTML'
        })


def user_manage_service(chat_id, user_chat_id, msg_id, language_code, callback_query_id):
    user_info = get_user_info(chat_id)

    if user_info != 'NOAUTH':
        language_code = user_info.language

    if user_info == 'NOAUTH' or not user_info.is_admin:
        controller.delete_message_thread(chat_id, msg_id)
        controller.answer_callback_query_with_dict(
            {'callback_query_id': callback_query_id, 'text': get_message(language_code)('com.noauth')})
        return

    target_user_info = get_user_info(user_chat_id)

    back_to_list_button = {'text': get_message(language_code)('usermanage.backtolist'),
                           'callback_data': 'user_manage_page 0'}

    if target_user_info == 'NOAUTH':
        controller.edit_message_with_dict({
            'chat_id': chat_id,
            'message_id': msg_id,
            'text': get_message(language_code)('usermanage.notsub'),
            'reply_markup': json.dumps({
                'inline_keyboard': [[back_to_list_button]]
            })
        })

    elif target_user_info.is_admin:
        controller.edit_message_with_dict({
            'chat_id': chat_id,
            'message_id': msg_id,
            'text': get_message(language_code)('usermanage.noaccessadm'),
            'reply_markup': json.dumps({
                'inline_keyboard': [[back_to_list_button]]
            })
        })

    else:
        inline_keyboard = [
            [{'text': get_message(language_code)('usermanage.prom'), 'callback_data': f'promote_confirm {user_chat_id}'},
             {'text': get_message(language_code)('usermanage.susp'), 'callback_data': f'suspend_confirm {user_chat_id}'}],
            [back_to_list_button]
        ]

        controller.edit_message_with_dict({
            'chat_id': chat_id,
            'message_id': msg_id,
            'text': get_message(language_code)('usermanage.default').format(
                chat_id=target_user_info.id,
                name=target_user_info.name,
                language=target_user_info.language,
                activity_state=get_message(language_code)(
                    'setting.active') if target_user_info.is_active else get_message(language_code)('setting.inactive')
            ),
            'reply_markup': json.dumps({
                'inline_keyboard': inline_keyboard
            }),
            'parse_mode': 'HTML'
        })


def promote_confirm_service(chat_id, user_chat_id, msg_id, language_code, callback_query_id):
    user_info = get_user_info(chat_id)

    if user_info != 'NOAUTH':
        language_code = user_info.language

    if user_info == 'NOAUTH' or not user_info.is_admin:
        controller.delete_message_thread(chat_id, msg_id)
        controller.answer_callback_query_with_dict(
            {'callback_query_id': callback_query_id, 'text': get_message(language_code)('com.noauth')})
        return

    target_user_info = get_user_info(user_chat_id)

    if target_user_info == 'NOAUTH':
        controller.delete_message_thread(chat_id, msg_id)
        controller.answer_callback_query_with_dict(
            {'callback_query_id': callback_query_id, 'text': get_message(language_code)('usermanage.notsub')})

    elif target_user_info.is_admin:
        controller.delete_message_thread(chat_id, msg_id)
        controller.answer_callback_query_with_dict(
            {'callback_query_id': callback_query_id, 'text': get_message(language_code)('usermanage.alr_admin')})

    else:
        inline_keyboard = [
            [{'text': get_message(language_code)('com.yes'), 'callback_data': f'promote {user_chat_id}'},
             {'text': get_message(language_code)('com.no'), 'callback_data': f'user_manage {user_chat_id}'}],
        ]

        controller.edit_message_with_dict({
            'chat_id': chat_id,
            'message_id': msg_id,
            'text': get_message(language_code)('usermanage.prom.confirm').format(target_user_info.name),
            'reply_markup': json.dumps({
                'inline_keyboard': inline_keyboard
            })
        })


def promote_service(chat_id, user_chat_id, msg_id, language_code, callback_query_id):
    user_info = get_user_info(chat_id)

    if user_info != 'NOAUTH':
        language_code = user_info.language

    if user_info == 'NOAUTH' or not user_info.is_admin:
        controller.delete_message_thread(chat_id, msg_id)
        controller.answer_callback_query_with_dict(
            {'callback_query_id': callback_query_id, 'text': get_message(language_code)('com.noauth')})
        return

    target_user_info = get_user_info(user_chat_id)

    if target_user_info == 'NOAUTH':
        controller.delete_message_thread(chat_id, msg_id)
        controller.answer_callback_query_with_dict(
            {'callback_query_id': callback_query_id, 'text': get_message(language_code)('usermanage.notsub')})

    elif target_user_info.is_admin:
        controller.delete_message_thread(chat_id, msg_id)
        controller.answer_callback_query_with_dict(
            {'callback_query_id': callback_query_id, 'text': get_message(language_code)('usermanage.alr_admin')})

    else:
        responsecode = update_user(user_chat_id, is_admin=True)

        if responsecode == '0000':
            controller.delete_message_thread(chat_id, msg_id)
            controller.answer_callback_query_with_dict(
                {'callback_query_id': callback_query_id, 'text': get_message(language_code)('com.success')})
            controller.send_message_with_dict(
                {'chat_id': target_user_info.id, 'text': get_message(language_code)('usermanage.prom.success')})

        else:
            controller.delete_message_thread(chat_id, msg_id)
            controller.answer_callback_query_with_dict(
                {'callback_query_id': callback_query_id, 'text': get_message(language_code)('com.failed')})


def suspend_confirm_service(chat_id, user_chat_id, msg_id, language_code, callback_query_id):
    user_info = get_user_info(chat_id)

    if user_info != 'NOAUTH':
        language_code = user_info.language

    if user_info == 'NOAUTH' or not user_info.is_admin:
        controller.delete_message_thread(chat_id, msg_id)
        controller.answer_callback_query_with_dict(
            {'callback_query_id': callback_query_id, 'text': get_message(language_code)('com.noauth')})
        return

    target_user_info = get_user_info(user_chat_id)

    if target_user_info != 'NOAUTH' and target_user_info.is_admin:
        controller.delete_message_thread(chat_id, msg_id)
        controller.answer_callback_query_with_dict(
            {'callback_query_id': callback_query_id, 'text': get_message(language_code)('usermanage.noaccessadm')})

    else:
        inline_keyboard = [
            [{'text': get_message(language_code)('usermanage.susp.option1'), 'callback_data': f'suspend suspend {user_chat_id}'},
             {'text': get_message(language_code)('usermanage.susp.option2'), 'callback_data': f'suspend block {user_chat_id}'}],
            [{'text': get_message(language_code)('com.no'),
              'callback_data': f'user_manage {user_chat_id}'}],
        ]

        controller.edit_message_with_dict({
            'chat_id': chat_id,
            'message_id': msg_id,
            'text': get_message(language_code)('usermanage.susp.confirm')
            .format(target_user_info.name),
            'reply_markup': json.dumps({
                'inline_keyboard': inline_keyboard
            })
        })


def suspend_service(chat_id, user_chat_id, msg_id, language_code, callback_query_id):
    user_info = get_user_info(chat_id)

    if user_info != 'NOAUTH':
        language_code = user_info.language

    if user_info == 'NOAUTH' or not user_info.is_admin:
        controller.delete_message_thread(chat_id, msg_id)
        controller.answer_callback_query_with_dict(
            {'callback_query_id': callback_query_id, 'text': get_message(language_code)('com.noauth')})
        return

    target_user_info = get_user_info(user_chat_id)

    if target_user_info != 'NOAUTH' and target_user_info.is_admin:
        controller.delete_message_thread(chat_id, msg_id)
        controller.answer_callback_query_with_dict(
            {'callback_query_id': callback_query_id, 'text': get_message(language_code)('usermanage.noaccessadm')})

    else:
        responsecode = delete_user(user_chat_id)

        if responsecode == '0000':
            controller.delete_message_thread(chat_id, msg_id)
            controller.answer_callback_query_with_dict(
                {'callback_query_id': callback_query_id, 'text': get_message(language_code)('com.success')})

        else:
            controller.delete_message_thread(chat_id, msg_id)
            controller.answer_callback_query_with_dict(
                {'callback_query_id': callback_query_id, 'text': get_message(language_code)('com.failed')})
