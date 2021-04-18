# -*- coding: utf-8 -*-
"""column configurations"""

__all__ = ['Column', 'ColumnGroup', 'align', 'default', 'sorter', 'type_', 'filter_', 'style']

from dataclasses import dataclass
from typing import Any, Optional, List, Dict

from . import align, default, sorter, type as type_, filter as filter_, style


@dataclass()
class Column:
    """Single column configuration"""
    key: str
    name: str
    type: type_.ColumnType
    editable: bool
    default: Any
    align: align.Alignment
    selection: Optional[List]
    sorter: sorter.Sorter
    filter: filter_.Filter
    style: style.Style

    @classmethod
    def from_cfg(cls, cfg):
        """Create Column from config dict"""
        fetcher = default.ValueFetcher(cfg)
        key = fetcher.get('key')
        return cls(
            key=key,
            name=fetcher.get('name', key),
            type=type_.ColumnType.make(fetcher),
            editable=fetcher.get('editable'),
            default=fetcher.get('default'),
            align=align.Alignment.make(fetcher),
            selection=fetcher.get('selection'),
            sorter=sorter.Sorter.make(fetcher),
            filter=filter_.Filter.make(fetcher),
            style=style.Style.make(fetcher),
        )

    def to_cfg(self):
        """Create config dict from Column"""
        return dict(
            key=self.key,
            name=self.name,
            type=self.type,
            editable=self.editable,
            default=self.default,
            h_align=self.align.h_align,
            v_align=self.align.v_align,
            selection=self.selection,
            sort_lt=self.sorter.sort_lt,
            filter_type=self.filter.type,
            color=self.style.color,
            bg_color=self.style.bg_color,
        )


class ColumnGroup:
    """Group of column configurations"""

    def __init__(self, column_config: List[Dict[str, Any]]):
        """Create list of Column from list of config dict"""
        try:
            self._columns = [Column.from_cfg(cfg)
                             for cfg in column_config]
        except Exception as e:
            raise ValueError(_cfg_error.format(str(e)))

    def __iter__(self):
        return iter(self._columns)

    def __len__(self):
        return len(self._columns)

    def config(self) -> List[Dict[str, Any]]:
        """Create list of config dict from list of Column"""
        return [column.to_cfg() for column in self]


_cfg_error = '''
Invalid column_config.
Following error found:
{error_msg}
'''


if __name__ == '__main__':
    pass
