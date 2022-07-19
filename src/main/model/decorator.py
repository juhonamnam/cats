from .base import db


def session_decorator(model_function):
    db.logger.info('EXECUTE: ' + model_function.__name__)
    def wrapper_function(*args, **kwargs):

        with db.Session() as session:

            try:
                result = model_function(*args, **kwargs, session=session)
            except Exception as e:
                session.rollback()
                db.logger.error(str(e))
                raise Exception("DATABASE_ERROR")

        return result

    return wrapper_function
