class Config(object):
    DEBUG = False


class ProductionConfig(Config):
    DATABASE_URI = "/root/EGEO.sqlite"
    CHANGELOG_URI = "dir of version log"


class DevelopmentConfig(Config):
    DEBUG = True
    CHANGELOG_URI = "dir of version log"
    DATABASE_URI = "" # Write the path to the database
