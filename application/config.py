import os


class Config(object):
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'default secret')


class ProductionConfig(Config):
    DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = True


configs = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
