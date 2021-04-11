# -*- coding: utf-8 -*-
"""doc string"""

__all__ = ['ValueFetcher']


class _DefaultColumn:
    type = str
    editable = True
    default = None
    h_align = 'l'
    v_align = 'c'
    selection = None
    sorting_proxy = None
    filter_type = 'contain'


class ValueFetcher:

    def __init__(self, config):
        self.config = config

    def get(self, key):
        return load(self.config, key)


def load(cfg, key):
    if key in cfg:
        return cfg[key]
    elif hasattr(_DefaultColumn, key):
        return getattr(_DefaultColumn, key)
    else:
        raise KeyError()


if __name__ == '__main__':
    pass
