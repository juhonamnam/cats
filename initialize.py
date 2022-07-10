from env import admin_id, admin_name
from src.main.model import initialize_db, new_user, user_count


def initialize():
    initialize_db()
    count =  user_count()
    if count == 0:
        new_user(id=int(admin_id), name=admin_name, is_admin=True, language='ko')
