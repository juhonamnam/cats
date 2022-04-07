from .en import en
from .ko import ko


def get_message(language_code):
    default = 'en'
    messages = {
        'en': en,
        'ko': ko
    }

    return lambda x: messages.get(language_code, messages.get(default, {})).get(x, x)
