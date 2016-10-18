class Config(object):
    TESTING = False
    DEBUG = False
    SECRET_KEY = 'development key'
    USERNAME = 'root'
    PASSWORD = ''


class ProductionConfig(Config):
    USERNAME = 'xana'
    PASSWORD = '123'

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    DEBUG =True
    TESTING = True


CLASS_ARRAY = [TestingConfig, DevelopmentConfig, ProductionConfig]

MyConfig = CLASS_ARRAY[0]
