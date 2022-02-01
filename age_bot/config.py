# built-in
import os
# 3rd party
from yaml2object import YAMLObject
from Ome


class Config(metaclass=YAMLObject):
    source = os.path.join(os.path.expanduser('~'), '.age_bot', 'config.yml')


class ServerDB(metaclass=YAMLObject):
    source = os.path.join(os.path.expanduser('~'), '.age_bot', 'serverdb.yml')
