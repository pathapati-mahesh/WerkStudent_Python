import configparser 
def load_config():
    """Reading the config.ini file using load_config"""
    config_obj = configparser.ConfigParser()
    config_obj.read("configurations\config.ini")
    return config_obj
