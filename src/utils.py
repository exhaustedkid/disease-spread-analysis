import typing as tp
from collections import defaultdict


def revert(dct: tp.Mapping[int, int]) -> dict[int, list[int]]:
    """
    :param dct: dictionary to revert in format {key: value}
    :return: reverted dictionary {value: [key1, key2, key3]}
    """
    result = defaultdict(list)
    for k, v in dct.items():
        result[v].append(k)

    return dict(result)
