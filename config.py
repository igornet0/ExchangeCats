import os
from dotenv import dotenv_values, load_dotenv

if not ".env" in os.listdir():
    with open(".env", "w") as f:
        for key, value in os.environ.items():
            f.write(f"{key}='{value}'")

dict_tokens = dotenv_values(".env")   

load_dotenv()

TOKEN_BOT_GAME = dict_tokens['TOKEN_BOT_GAME']
LINK_BOT_GAME = dict_tokens['LINK_BOT_GAME']

EXCHANGE_URL = dict_tokens['EXCHANGE_URL']
TOKEN_BOT_EXCHANGE = dict_tokens['TOKEN_BOT_EXCHANGE']
LINK_BOT_EXCHANGE = dict_tokens['LINK_BOT_EXCHANGE']

TOKEN_BOT_CASINO = dict_tokens['TOKEN_BOT_CASINO']
LINK_BOT_CASINO = dict_tokens['LINK_BOT_CASINO']

class Config(object):
    MYSQL_ROOT_PASSWORD = os.getenv('MYSQL_ROOT_PASSWORD')
    MYSQL_ROOT = os.getenv('MYSQL_ROOT')
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = True if os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS') else False


class DevelopmentConfig(Config):
    """
    Development configurations
    """

    DEBUG = True
    SQLALCHEMY_ECHO = True


class ProductionConfig(Config):
    """
    Production configurations
    """

    DEBUG = False


app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}