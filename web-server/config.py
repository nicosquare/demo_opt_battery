class Config(object):
    DEBUG = False


class ProductionConfig(Config):
    DATABASE_URI = "./"
    CHANGELOG_URI = "./"


class DevelopmentConfig(Config):
    DEBUG = True
    CHANGELOG_URI = "./"
    DATABASE_URI = "" # Write the path to the database
