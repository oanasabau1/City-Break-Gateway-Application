import os


db_user = os.environ.get('DB_USER') or 'myuser'
db_password = os.environ.get('DB_PASSWORD') or 'mypassword'
db_host = os.environ.get('DB_HOST') or 'localhost'
db_name = os.environ.get('DB_NAME') or 'citybreak'

db_url = f'mysql://{db_user}:{db_password}@{db_host}/{db_name}'
