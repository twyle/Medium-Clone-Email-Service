import os
from dotenv import load_dotenv

load_dotenv()


class BaseConfig:
    DEBUG = True
    TESTING = False
    
    SECRET_KEY=os.getenv('SECRET_KEY', 'super-secret-key')
    
    MAIL_USERNAME=os.environ['MAIL_USERNAME']
    MAIL_PASSWORD=os.environ['MAIL_PASSWORD']
    MAIL_SERVER=os.environ['MAIL_SERVER']
    MAIL_PORT=os.environ['MAIL_PORT']
    MAIL_USE_SSL=os.environ['MAIL_USE_SSL']
    
    POSTGRES_HOST = os.environ['POSTGRES_HOST']
    POSTGRES_DB = os.environ['POSTGRES_DB']
    POSTGRES_PORT = os.environ['POSTGRES_PORT']
    POSTGRES_USER = os.environ['POSTGRES_USER']
    POSTGRES_PASSWORD = os.environ['POSTGRES_PASSWORD']

    db_conn_string = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    SQLALCHEMY_DATABASE_URI = db_conn_string
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(BaseConfig):
    """Configuration used during development."""
    SECRET_KEY=os.getenv('SECRET_KEY', 'super-secret-key')


class TestingConfig(BaseConfig):
    """Configuration used during development."""
    SECRET_KEY=os.getenv('SECRET_KEY', 'super-secret-key')


class StagingConfig(BaseConfig):
    """Configuration used during development."""
    SECRET_KEY=os.getenv('SECRET_KEY', 'super-secret-key')


class ProductionConfig(BaseConfig):
    """Configuration used during development."""
    SECRET_KEY=os.getenv('SECRET_KEY', 'super-secret-key')