import sys
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv('CATS_TELE_KEY')
admin_id = os.getenv('CATS_INITIAL_ADMIN_ID')
admin_name = os.getenv('CATS_INITIAL_ADMIN_NAME', 'First Admin')
sql_url = os.getenv('CATS_SQL_URL', 'sqlite:///test.db?check_same_thread=False')
is_production = len(sys.argv) > 1 and sys.argv[1] == 'production'
