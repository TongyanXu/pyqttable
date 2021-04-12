# -*- coding: utf-8 -*-
"""doc string"""

__all__ = ['SortStatus', 'Sorter']

import enum
import pandas as pd

from .default import ValueFetcher
from typing import Optional


class SortStatus(enum.Enum):
    Nothing = 0
    Ascending = 1
    Descending = 2


class SortProxy:

    def __init__(self, value, lt):
        self.value = value
        self._lt = lt

    @classmethod
    def create(cls, value, lt):
        return cls(value, lt)

    def __lt__(self, other):
        return self._lt(self.value, other.value)


class Sorter:

    def __init__(self, sort_lt: Optional[callable]):
        self.sort_lt = sort_lt

    @classmethod
    def make(cls, fetcher: ValueFetcher):
        return cls(fetcher.get('sort_lt'))

    def sort_data(self, df: pd.DataFrame, by: str, status: SortStatus):
        df = df.copy()

        if self.sort_lt is not None:
            proxy = df[by].apply(SortProxy.create, lt=self.sort_lt)
            by = f'{by}_sorting_proxy'
            df[by] = proxy

        if status == SortStatus.Ascending:
            res = df.sort_values(by=by)
        elif status == SortStatus.Descending:
            res = df.sort_values(by=by, ascending=False)
        else:
            res = df.sort_index()

        if self.sort_lt is not None:
            res.drop(by, axis=1, inplace=True)

        return res


if __name__ == '__main__':
    pass
