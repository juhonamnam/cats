import sys
import os

api_key = os.getenv('TELE_KEY')
sql_url = os.getenv('SQL_URL')
is_production = len(sys.argv) > 1 and sys.argv[1] == 'production'
