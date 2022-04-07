from src.resources.message import get_message
from src.main.controller import controller
from src.main.model import get_user_info


def about_service(chat_id, language_code, msg_id):
    user_info = get_user_info(chat_id)

    if user_info != 'NOAUTH':
        language_code = user_info.language

    controller.delete_message_thread(chat_id, msg_id)
    controller.send_message_with_dict({
        'chat_id': chat_id,
        'text': get_message(language_code)('about'),
        'parse_mode': 'HTML'
    })
