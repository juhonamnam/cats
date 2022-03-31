import os
from src.main.model import initialize_db, new_user

admin_id = os.getenv('cats_initial_admin_id')
admin_name = os.getenv('cats_initial_admin_name', 'First Admin')

if __name__ == '__main__':
    initialize_db()
    new_user(id=int(admin_id), name=admin_name, is_admin=True, language='ko')
