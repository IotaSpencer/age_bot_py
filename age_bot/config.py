# built-in
import os
# 3rd party
from yaml2object import YAMLObject
from omegaconf import OmegaConf

class Configs:
    def Config():
    src_path = os.path.join(os.path.expanduser('~'), '.age_bot', 'config.yml')
    return OmegaConf.load(src_path)


    def ServerDB(metaclass=YAMLObject):
     = os.path.join(os.path.expanduser('~'), '.age_bot', 'serverdb.yml')
