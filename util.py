import configparser
import argparse
import pathlib

def load_config(configfile, section):
    home = pathlib.Path.home()
    config = configparser.ConfigParser()
    config.read(pathlib.Path.home().joinpath(configfile))
    cfg = {}
    for key in config[section]:
        cfg[key] = config[section][key]
    return cfg

def create_argparser(prog):
    parser = argparse.ArgumentParser(prog='python3 {}'.format(prog))
    parser.add_argument('-f', '--from', help='datum -tol, pl.: "2021.01.01"', dest='datefrom')
    parser.add_argument('-t', '--to', help='datum -ig, pl.: "2021.01.31"', dest='dateto')
    parser.add_argument('-d', '--download', help='celmappa letolteshez', dest='downloadpath')
    return parser