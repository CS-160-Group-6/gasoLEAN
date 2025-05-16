## System Overview

- **python-OBD**: A client library for interacting with ELM327-style adapters; it auto-scans for Bluetooth/USB serial ports, performs a standard AT-command handshake, and parses responses into unit-bearing `OBDResponse` objects via Pint :contentReference[oaicite:2]{index=2}.

## Core Components & Flows

### Connection Management

- **python-OBD** auto-detects adapters (or accepts an explicit port string). On `OBD()` instantiation it sends AT commands (`ATZ`, `ATE0`, `ATL0`, `ATH1`, etc.) and probes Mode 01 PIDs to build its supported-commands table :contentReference[oaicite:5]{index=5}:contentReference[oaicite:6]{index=6}.

### Command Lookup & Execution

- **python-OBD** exposes `obd.commands` (Mode × PID), introspection helpers (`has_pid()`, `has_name()`), and supports custom `OBDCommand` objects for arbitrary PIDs :contentReference[oaicite:7]{index=7}:contentReference[oaicite:8]{index=8}.  
- **Integration**: Calling `connection.query(cmd)` in python-OBD sends raw hex (e.g. `010C\r`), which the emulator matches against its `Request` patterns and replies as configured.

## Asynchronous & Monitoring APIs

- **python-OBD.Async**: A subclass of `OBD` that maintains a background thread to refresh watched commands; use `watch(cmd)`, `start()`, and non-blocking `query()` calls, with optional callbacks on new data :contentReference[oaicite:17]{index=17}:contentReference[oaicite:18]{index=18}.  

## Logging & Diagnostics

- **python-OBD** logs every AT/OBD exchange at `DEBUG` via `obd.logger` and can dump raw traces to stderr for troubleshooting :contentReference[oaicite:19]{index=19}:contentReference[oaicite:20]{index=20}.  
