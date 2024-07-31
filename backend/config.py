import os

ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 30 minutes
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days
ALGORITHM = "HS256"

# Both keys should be kept secret
JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'secret')
JWT_REFRESH_SECRET_KEY = os.environ.get('JWT_REFRESH_SECRET_KEY', 'refresh_secret')

MONGODB_HOST = os.environ.get('MONGO_HOST', 'mongo')  # Default to 'mongo' if not set
MONGODB_PORT = int(os.environ.get('MONGO_PORT', 27017))  # Default to 27017
MONGODB_USER = os.environ.get('MONGO_USER')  # Optional username
MONGODB_PASSWORD = os.environ.get('MONGO_PASSWORD')  # Optional password
MONGODB_DB = os.environ.get('MONGO_DB', 'knorozovDb')  # Default to 'knorozovDb'

connection_string = f"mongodb://{MONGODB_HOST}:{MONGODB_PORT}"

if MONGODB_USER and MONGODB_PASSWORD:
    connection_string = f"mongodb://{MONGODB_USER}:{MONGODB_PASSWORD}@{MONGODB_HOST}:{MONGODB_PORT}"

database_name = MONGODB_DB