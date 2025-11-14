"""RemoteProxy: dynamic client-side proxy for remote objects."""
from __future__ import annotations
import json
import socket
from typing import Any, Callable

class RemoteProxy:
    def __init__(self, object_name: str, host: str = "127.0.0.1", port: int = 5000, timeout: float = 5.0):
        self._object_name = object_name
        self._host = host
        self._port = port
        self._timeout = timeout

    def __getattr__(self, method_name: str) -> Callable:
        def _remote_call(*args, **kwargs) -> Any:
            request = {
                "object": self._object_name,
                "method": method_name,
                "args": args,
                "kwargs": kwargs,
            }
            with socket.create_connection((self._host, self._port), timeout=self._timeout) as sock:
                sock.sendall(json.dumps(request).encode("utf-8"))
                raw = sock.recv(65536)
            if not raw:
                raise ConnectionError("Empty response from server")
            response = json.loads(raw.decode("utf-8"))
            if response.get("status") == "ok":
                return response.get("result")
            raise RuntimeError(response.get("error", "Unknown remote error"))
        return _remote_call
