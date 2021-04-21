"""Ganttic API client.

Dribia 2021/04/21, Oleguer Sagarra Pascual <ula@dribia.com>
"""

try:
    from importlib.metadata import version  # type: ignore
except ModuleNotFoundError:
    from importlib_metadata import version  # type: ignore

__version__ = version(__name__)
