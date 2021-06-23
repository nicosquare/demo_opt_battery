
class Config(object):
    DEBUG = False


class ProductionConfig(Config):
    DATABASE_URI = "/root/CVM.sqlite"
    CHANGELOG_URI = "dir of version log"
    DATA_ENERGY_URI = "/root/energy_data/"
    DATA_ELECTRIC_URI = "/root/electric_data/"
    DATA_HARMONIC_URI = "/root/harmonic_data/"
    DATA_CREG_015_URI = "/root/creg_015/"


class DevelopmentConfig(Config):
    DEBUG = True
    DATABASE_URI = ""
    DATA_ENERGY_URI = ""
    DATA_ELECTRIC_URI = ""
    DATA_HARMONIC_URI = ""
    DATA_CREG_015_URI = ""
    CHANGELOG_URI = "dir of version log"

