# OOP Middleware (Simple RMI over TCP)

A minimal Object-Oriented middleware layer enabling Remote Method Invocation (RMI) between a Python client and server using sockets + JSON.

## Components

- `remote_base.py` – Defines `RemoteObject` base class.
- `server.py` – `RemoteServer` registers objects and dispatches method calls.
- `client.py` – `RemoteProxy` dynamically forwards local attribute access to the server.
- `calculator.py` – Example remote object.
- `demo.py` – Starts server and issues sample remote calls.

## Protocol

Client sends a single JSON object per request:
```json
{
  "object": "calc",
  "method": "add",
  "args": [5, 7],
  "kwargs": {}
}
```
Server responds:
```json
{"status": "ok", "result": 12}
```
Errors:
```json
{"status": "error", "error": "Division by zero"}
```

## Run Demo

```bash
python demo.py
```

Or start server manually:
```bash
python server.py
```
Then in another Python session:
```python
from client import RemoteProxy
calc = RemoteProxy("calc")
print(calc.multiply(3,4))
```

## Extending

1. Create a subclass of `RemoteObject` with public methods.
2. Register it: `server.register("name", instance)`.
3. Use `RemoteProxy("name")` to access its methods.

## Notes
- Single-request per connection (simple, stateless).
- JSON serialization only (custom types must be converted manually).
- Add authentication / encryption as needed (e.g., TLS or signing).
