import pip
from yaml import safe_load as load
from munch import DefaultMunch

config = DefaultMunch.fromDict(
            load(open('config.yaml')),
                object())
