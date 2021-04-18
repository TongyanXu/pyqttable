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
    sort_lt = None
    filter_type = 'contain'
    color = None
    bg_color = None


class ValueFetcher:

    def __init__(self, config):
        self.config = config

    def get(self, key, default=None):
        return load(self.config, key, default)


def load(cfg, key, dft=None):
    if key in cfg and cfg[key] is not None:
        return cfg[key]
    elif dft is not None:
        return dft
    elif hasattr(_DefaultColumn, key):
        return getattr(_DefaultColumn, key)
    else:
        raise KeyError(f'Missing key \'{key}\'')


if __name__ == '__main__':
    pass
