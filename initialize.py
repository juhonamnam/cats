import os
from src.main.model import initialize_db, new_user

admin_id = os.getenv('CATS_INITIAL_ADMIN_ID')
admin_name = os.getenv('CATS_INITIAL_ADMIN_NAME', 'First Admin')

if __name__ == '__main__':
    initialize_db()
    new_user(id=int(admin_id), name=admin_name, is_admin=True, language='ko')
