# -*- coding: utf-8 -*-
"""default configuration"""

__all__ = ['ValueFetcher']


class _DefaultColumn:
    """Common default config"""
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
    """Fetcher to get value from config dict"""

    def __init__(self, config):
        self.config = config

    def get(self, key, default=None):
        """Get config by key"""
        return load(self.config, key, default)


def load(cfg, key, dft=None):
    # Find value in config dict
    if key in cfg and cfg[key] is not None:
        return cfg[key]

    # Use override default if given
    elif dft is not None:
        return dft

    # Find value in default config
    elif hasattr(_DefaultColumn, key):
        return getattr(_DefaultColumn, key)

    # Key not found, raise error
    else:
        raise KeyError(f'Missing key \'{key}\'')


if __name__ == '__main__':
    pass
