# gasoLEAN Backend

This backend service powers **gasoLEAN**, a vehicle analytics platform that interfaces with real or emulated OBD-II (On-Board Diagnostics) data. It decodes VIN information, monitors vehicle telemetry, and stores ride statistics using a RESTful API built on FastAPI, SQLAlchemy ORM, and the ELM327 emulator.

The system is structured for maintainability and modularity, with logical separation between routing, core business logic, database models, and emulator control.

---

## Project Overview

This backend enables features including:

- VIN retrieval from OBD (real or emulated)
- Persistent storage of vehicle metadata
- Ride session creation, fuel usage tracking, and scoring
- Real-time measurement capture via PID commands
- Modular API routing and schema validation using FastAPI and Pydantic

---

## Installation and Setup

Follow the steps below to install, configure, and run the backend.
To run with real time data and see the full functionality of the application you need a OBD-II device configured and running in your car.

## Project Structure

backend/
│
├── app/
│   ├── main.py               # FastAPI entrypoint
│   ├── config.py             # Settings loader (env, DB config)
│   ├── core/                 # Business logic like OBD integration and scoring
│   ├── db/                   # SQLAlchemy models, sessions, and CRUD operations
│   ├── api/                  # All API versioned routes and schemas
│   ├── services/             # Background services for measurement streams
│   └── vinner/               # VIN decoder + NHTSA API integration
│
├── scripts/
│   └── simulate.py           # Emulator data simulation script
│
├── data.db                   # SQLite database (can be deleted/regenerated)
├── elm.log                   # Emulator log file
├── requirements.txt          # Python dependencies
└── README.md                 # You are here!



### SETUP

git clone <your-repository-url>
cd backend

python3 -m venv myenv
source myenv/bin/activate

pip install -r app/requirements.txt

uvicorn app.main:app --reload

http://localhost:8000/docs      # Interactive API docs (Swagger UI)
http://localhost:8000/api/v1    # API base path


## Emulator Integration

The backend uses an ELM327 emulator (v3.0.4) to simulate vehicle telemetry. When launched:

- It starts the emulator
- Injects a 17-character VIN using `Edit(emulator, pid="VIN", val="...")`
- Responds to Mode 09 PID 02 queries with a valid VIN

The VIN is then decoded via the NHTSA API and stored.

The emulator is auto-invoked when FastAPI starts, and no separate step is needed.

## Environment Configuration

If needed, you can configure runtime settings via a `.env` file inside the `app/` directory:

DATABASE_URL=sqlite:///../data.db
EMULATOR_MODE=true


## Key Functional Components

### obd_integration.py

- Connects to the emulator or real OBD port
- Injects test VINs using the emulator's `Edit` command
- Queries VIN and passes it to the VIN decoder

### vinner/decoder.py

- Sends the retrieved VIN to the National Highway Traffic Safety Administration (NHTSA) API
- Extracts and returns details like make, model, model year, and vehicle type

### db/models.py

- ORM classes for `Vehicle`, `Ride`, `Measurement`, and `Profile`
- Defines primary and foreign key relationships and default fields

### crud/vehicle.py

- Provides functionality to get, create, list, and delete vehicle records
- Ensures a VIN is only stored once

### api/v1/routers/

- Routes are modular and versioned under `/api/v1`
- Includes endpoints for health checks, ride tracking, profile management, and vehicle VIN decoding

### scripts/simulate.py

- Used to simulate real-time data streams from the emulator
- Useful for testing ride sessions without a physical car

## Running the API

To interact with the API after starting the server, use the following sample endpoints:

| Method | Endpoint                             | Description                               |
|--------|--------------------------------------|-------------------------------------------|
| GET    | `/api/v1/vehicle/info`               | Decodes and returns vehicle info by VIN   |
| GET    | `/api/v1/rides/`                     | Lists all rides                           |
| POST   | `/api/v1/rides/`                     | Starts a new ride                         |
| DELETE | `/api/v1/vehicle/by-vin/{vin}`       | Deletes a vehicle by VIN                  |
| GET    | `/api/v1/health`                     | Health check                              |

API documentation is automatically generated and accessible via Swagger UI at:
http://localhost:8000/docs

