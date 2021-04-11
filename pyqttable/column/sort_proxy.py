# -*- coding: utf-8 -*-
"""doc string"""

__all__ = ['SortStatus', 'SortingProxy']

import enum
import pandas as pd

from pyqttable.column.default import ValueFetcher
from typing import Optional


class SortStatus(enum.Enum):
    Nothing = 0
    Ascending = 1
    Descending = 2


class SortingProxy:

    def __init__(self, sorting_proxy: Optional[callable]):
        self.sorting_proxy = sorting_proxy
        self._make_proxy = self.sorting_proxy is not None

    @classmethod
    def make(cls, fetcher: ValueFetcher):
        return cls(
            sorting_proxy=fetcher.get('sorting_proxy'),
        )

    def sort_data(self, df: pd.DataFrame, by: str, status: SortStatus):
        if self._make_proxy:
            proxy = df[by].apply(self.sorting_proxy)
            by = f'{by}_sorting_proxy'
            df = df.copy()
            df[by] = proxy

        if status == SortStatus.Ascending:
            res = df.sort_values(by=by)
        elif status == SortStatus.Descending:
            res = df.sort_values(by=by, ascending=False)
        else:
            res = df.sort_index()

        if self._make_proxy:
            res.drop(by, axis=1, inplace=True)

        return res


if __name__ == '__main__':
    pass
