"""This is the module that defines the common process.
"""

from logging import getLogger
from typing import Any

from lib.common.types import ParamLog

PARAM_LOG = ParamLog()
LOGGER = getLogger(PARAM_LOG.NAME)


def recursive_replace(data: Any, fm_val: Any, to_val: Any) -> Any:
    """Performs a recursive replacement.

    Args:
        data (Any): data before replacement.
        fm_val (Any): value before replacement.
        to_val (Any): value after replacement.

    Returns:
        Any: data after replacement.
    """
    if isinstance(data, dict):
        return {
            key: recursive_replace(
                data=val,
                fm_val=fm_val,
                to_val=to_val,
            ) for key, val in data.items()
        }
    if isinstance(data, list):
        return [
            recursive_replace(
                data=val,
                fm_val=fm_val,
                to_val=to_val,
            ) for val in data
        ]
    if isinstance(data, tuple):
        return tuple(
            recursive_replace(
                data=val,
                fm_val=fm_val,
                to_val=to_val,
            ) for val in data
        )
    if isinstance(data, set):
        return {
            recursive_replace(
                data=val,
                fm_val=fm_val,
                to_val=to_val,
            ) for val in data
        }
    if data == fm_val:
        return to_val
    return data


def sec_to_hms(time: float) -> tuple[int, int, int, float]:
    """Convert seconds to hh:mm:ss:ms format.

    Args:
        time (float): The number of seconds.

    Returns:
        tuple[int, int, int, float]: The tuple of hh, mm, ss, ms.
    """
    hh, mm = divmod(time, 3600)
    mm, ss = divmod(mm, 60)
    ss, ms = divmod(ss, 1)
    return hh, mm, ss, ms
