# -*- coding: utf-8 -*-
"""column sorter"""

__all__ = ['SortStatus', 'Sorter']

import enum
import pandas as pd

from .default import ValueFetcher
from typing import Optional


class SortStatus(enum.Enum):
    """Sorting status"""
    Nothing = 0
    Ascending = 1
    Descending = 2


class SortProxy:
    """
    Column sorting proxy to realized custom sorting
    SortProxy is a wrapper of cell value but use customized sort_lt as __lt__
    Pandas DataFrame is calling __lt__ for sorting
    Replacement of __lt__ can lead to customized sorting activities
    """

    def __init__(self, value, lt):
        self.value = value
        self._lt = lt

    @classmethod
    def create(cls, value, lt):
        return cls(value, lt)

    def __lt__(self, other):
        return self._lt(self.value, other.value)


class Sorter:
    """Column sorter to sort data in customized way"""

    def __init__(self, sort_lt: Optional[callable]):
        self.sort_lt = sort_lt

    @classmethod
    def make(cls, fetcher: ValueFetcher):
        """Make Sorter from ValueFetcher"""
        return cls(fetcher.get('sort_lt'))

    def sort_data(self, df: pd.DataFrame, by: str, status: SortStatus) -> pd.DataFrame:
        """
        Sort data in customized way

        Parameters
        ----------
        df: DataFrame to be sorted
        by: column key to sort by
        status: sorting status

        Returns
        -------
        Sorted DataFrame
        """
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
