from __future__ import annotations
import abc
from typing import Any

class RemoteObject(abc.ABC):
    def allow_call(self, method_name: str) -> bool:
        return not method_name.startswith("_")

    def pre_invoke(self, method_name: str, args: tuple, kwargs: dict) -> None:
        pass

    def post_invoke(self, method_name: str, result: Any) -> Any:
        return result
