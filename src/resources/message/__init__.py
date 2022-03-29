from .en import en


def get_message(language_code):
    default = 'en'
    messages = {
        'en': en
    }

    return lambda x: messages.get(language_code, messages.get(default, {})).get(x, x)
