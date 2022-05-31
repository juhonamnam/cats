from env import admin_id, admin_name
from src.main.model import initialize_db, new_user

if __name__ == '__main__':
    initialize_db()
    new_user(id=int(admin_id), name=admin_name, is_admin=True, language='ko')
