# built-in
import os
from dataclasses import dataclass
# 3rd party
from typing import Union

from omegaconf import OmegaConf, DictConfig, ListConfig

config_path = os.path.join(os.path.expanduser('~'), '.age_bot', 'config.yml')
dev_config_path = os.path.join(os.path.expanduser('~'), '.age_bot', 'dev-config.yml')
sdb_path = os.path.join(os.path.expanduser('~'), '.age_bot', 'serverdb.yml')
webhook_config = os.path.join(os.path.expanduser('~'), '.logger_hook.yml')

@dataclass
class Configs:
    cfg: Union[DictConfig, ListConfig] = OmegaConf.load(config_path)
    dcfg: Union[DictConfig, ListConfig] = OmegaConf.load(dev_config_path)
    sdb: Union[DictConfig, ListConfig] = OmegaConf.load(sdb_path)
    hook: Union[DictConfig, ListConfig] = OmegaConf.load(webhook_config)