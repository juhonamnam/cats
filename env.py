import sys
import os

api_key = os.getenv('TELE_KEY')
admin_id = os.getenv('INITIAL_ADMIN_ID')
admin_name = os.getenv('INITIAL_ADMIN_NAME', 'First Admin')
sql_url = os.getenv('SQL_URL')
is_production = len(sys.argv) > 1 and sys.argv[1] == 'production'
