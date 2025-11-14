import json, socket, threading, traceback
from typing import Dict
from remote_base import RemoteObject

class RemoteServer:
    def __init__(self, host="127.0.0.1", port=5000):
        self.host, self.port = host, port
        self.sock = socket.socket()
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.objects: Dict[str, RemoteObject] = {}
        self.running = False

    def register(self, name, obj):
        if name in self.objects:
            raise ValueError("duplicate object name")
        self.objects[name] = obj

    def start(self):
        self.sock.bind((self.host, self.port))
        self.sock.listen()
        self.running = True
        print(f"Server listening on {self.host}:{self.port}")
        threading.Thread(target=self._loop, daemon=True).start()

    def stop(self):
        self.running = False
        self.sock.close()

    def _loop(self):
        while self.running:
            try:
                conn, _ = self.sock.accept()
            except OSError:
                return
            threading.Thread(target=self._handle, args=(conn,), daemon=True).start()

    def _handle(self, conn):
        try:
            raw = conn.recv(65536)
            if not raw:
                return
            try:
                req = json.loads(raw.decode())
            except json.JSONDecodeError:
                return conn.sendall(b'{"status":"error","error":"invalid json"}')
            conn.sendall(json.dumps(self._dispatch(req)).encode())
        finally:
            conn.close()

    def _dispatch(self, req):
        obj = self.objects.get(req.get("object"))
        if not obj:
            return {"status": "error", "error": "unknown object"}
        method = getattr(obj, req.get("method", ""), None)
        if not callable(method) or not obj.allow_call(method.__name__):
            return {"status": "error", "error": "bad method"}
        try:
            obj.pre_invoke(method.__name__, req.get("args", ()), req.get("kwargs", {}))
            result = method(*req.get("args", ()), **req.get("kwargs", {}))
            return {"status": "ok", "result": obj.post_invoke(method.__name__, result)}
        except Exception as ex:
            return {"status": "error", "error": str(ex), "trace": traceback.format_exc()}

if __name__ == "__main__":
    from calculator import Calculator
    s = RemoteServer()
    s.register("calc", Calculator())
    s.start()
    try:
        while True:
            threading.Event().wait(1)
    except KeyboardInterrupt:
        s.stop()
