class Config(object):
    """Parent configuration class."""
    DEBUG = False
    CSRF_ENABLED = True


class DevelopmentConfig(Config):
    """Configurations for Development."""
    DEBUG = True


class TestingConfig(Config):
    """Configurations for Test environment."""
    TESTING = True
    DEBUG = True


class ProductionConfig(Config):
    """Configurations for Production."""
    DEBUG = False
    TESTING = False


app_config = {
    'dev': DevelopmentConfig,
    'test': TestingConfig,
    'production': ProductionConfig,
}
