class PostgreSqlConfig:
    DB_USER = 'ivan'
    DB_PASSWORD = '12'
    DB_HOST = 'localhost'
    DB_NAME = 'upark'
    DB_PORT = '5432'

    # DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    DATABASE_URL = "postgresql://postgres:postgres@parking_postgres:5432/upark"  # docker


class BotConfig:
    token = "1970953610:AAFM4WUUei8okYTWghAub1SmnuGJ-pYpuw8"


class RedisConfig:
    URL = 'redis://parking_redis:6379'  # docker
    # URL = 'redis://0.0.0.0:6379'  # local
    DB = '0'
    PASSWORD = "password"

