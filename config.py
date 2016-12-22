class Config(object):
    TESTING = False
    DEBUG = False
    SECRET_KEY = 'BnUcbCUHZj3lzrdHutfAI5cRCBLzBY3JIAIxt2ZWUz8='
    USERNAME = 'root'
    PASSWORD = ''
    UNIX_SOCKET = ''

class ProductionConfig(Config):
    USERNAME = 'xana'
    PASSWORD = '123'

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    DEBUG = True
    TESTING = True

class TempDevelopmentConfig(Config):
    DEBUG = True
    UNIX_SOCKET = '/var/run/mysqld/mysqld.sock'


CLASS_ARRAY = [TestingConfig, DevelopmentConfig, ProductionConfig, TempDevelopmentConfig]

MyConfig = CLASS_ARRAY[0]
