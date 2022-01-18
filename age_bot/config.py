from yaml2object import YAMLObject
import os
class Config(metaclass=YAMLObject):
    source = os.path.join(os.path.expanduser('~'), '.age_bot', 'config.yml')
