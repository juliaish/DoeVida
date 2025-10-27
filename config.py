import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "chave_fallback_para_dev")
    DATABASE = "meubanco.db"

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    DATABASE = "test.db"

class ProductionConfig(Config):
    DEBUG = False
