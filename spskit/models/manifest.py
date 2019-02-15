import itertools
from copy import deepcopy
from io import BytesIO
import re
from typing import Union, Callable, Any, Tuple
from datetime import datetime

from . import exceptions


def utcnow():
    return str(datetime.utcnow().isoformat() + "Z")


class Manifest:
    """Namespace para funções que manipulam maços.
    """

    @staticmethod
    def new(bundle_id: str, now: Callable[[], str] = utcnow) -> dict:
        timestamp = now()
        return {
            "id": str(bundle_id),
            "created": timestamp,
            "updated": timestamp,
            "metadata": {},
        }

    @staticmethod
    def set_metadata(
        bundle: dict,
        name: str,
        value: Union[dict, str],
        now: Callable[[], str] = utcnow,
    ) -> dict:
        _bundle = deepcopy(bundle)
        _now = now()
        metadata = _bundle["metadata"].setdefault(name, [])
        metadata.append((_now, value))
        _bundle["updated"] = _now
        return _bundle

    @staticmethod
    def get_metadata(bundle: dict, name: str, default="") -> Any:
        try:
            return bundle["metadata"].get(name, [])[-1][1]
        except IndexError:
            return default

    @staticmethod
    def get_metadata_all(bundle: dict, name: str) -> Any:
        try:
            return bundle["metadata"].get(name, [])
        except IndexError:
            return default
