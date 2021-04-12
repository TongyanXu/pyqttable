# -*- coding: utf-8 -*-
"""doc string"""

__all__ = ['Column', 'align', 'default', 'sorter', 'type_', 'filter']

from dataclasses import dataclass
from typing import Any, Optional, List

from . import align
from . import default
from . import sorter
from . import type as type_
from . import filter


@dataclass()
class Column:
    key: str
    name: str
    type: type_.ColumnType
    editable: bool
    default: Any
    align: align.Alignment
    selection: Optional[List]
    sorter: sorter.Sorter
    filter: filter.Filter

    @classmethod
    def from_cfg(cls, cfg):
        fetcher = default.ValueFetcher(cfg)
        return cls(
            key=fetcher.get('key'),
            name=fetcher.get('name'),
            type=type_.ColumnType.make(fetcher),
            editable=fetcher.get('editable'),
            default=fetcher.get('default'),
            align=align.Alignment.make(fetcher),
            selection=fetcher.get('selection'),
            sorter=sorter.Sorter.make(fetcher),
            filter=filter.Filter.make(fetcher),
        )

    def to_cfg(self):
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
        )


if __name__ == '__main__':
    pass
