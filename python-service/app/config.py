import os


class BaseConfig:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key")
    JWT_ACCESS_TOKEN_EXPIRES = 3600


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://"
        f"{os.environ.get('DATABASE_USER', 'appuser')}:"
        f"{os.environ.get('DATABASE_PASSWORD', 'apppassword')}@"
        f"localhost:"
        f"{os.environ.get('DATABASE_PORT', '5432')}/"
        f"{os.environ.get('DATABASE_NAME', 'ecommerce')}"
    )


class StagingConfig(BaseConfig):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://"
        f"{os.environ.get('DB_USER', 'appuser')}:"
        f"{os.environ.get('DB_PASS', 'apppassword')}@"
        f"{os.environ.get('DB_HOST', 'localhost')}:"
        f"{os.environ.get('DB_PORT', '5432')}/"
        f"{os.environ.get('DB_NAME', 'ecommerce')}"
    )


class ProductionConfig(BaseConfig):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://"
        f"{os.environ.get('DB_USER', 'appuser')}:"
        f"{os.environ.get('DB_PASS', 'apppassword')}@"
        f"{os.environ.get('DB_HOST', 'localhost')}:"
        f"{os.environ.get('DB_PORT', '5432')}/"
        f"{os.environ.get('DB_NAME', 'ecommerce')}"
    )


class TestingConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    JWT_SECRET_KEY = "test-secret-key"


config_map = {
    "development": DevelopmentConfig,
    "staging": StagingConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
}


def get_config(config_name=None):
    if config_name is None:
        config_name = os.environ.get("FLASK_ENV", "development")
    return config_map.get(config_name, DevelopmentConfig)
