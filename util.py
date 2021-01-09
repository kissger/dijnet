import configparser
import pathlib

def load_config(configfile):
    home = pathlib.Path.home()
    config = configparser.ConfigParser()
    config.read(pathlib.Path.home().joinpath(configfile))
    cfg = {}
    for key in config['AUTH']:
        cfg[key] = config['AUTH'][key]
    return cfg