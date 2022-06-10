# built-in
import os
from dataclasses import dataclass
# 3rd party
from typing import Union

from omegaconf import OmegaConf, DictConfig, ListConfig

config_path = os.path.join(os.path.expanduser('~'), '.age_bot', 'config.yml')
dev_config_path = os.path.join(os.path.expanduser('~'), '.age_bot', 'dev-config.yml')
sdb_path = os.path.join(os.path.expanduser('~'), '.age_bot', 'serverdb.yml')


@dataclass
class Configs:
    config: Union[DictConfig, ListConfig] = OmegaConf.load(config_path)
    devconfig: Union[DictConfig, ListConfig] = OmegaConf.load(dev_config_path)
    serverdb: Union[DictConfig, ListConfig] = OmegaConf.load(sdb_path)
