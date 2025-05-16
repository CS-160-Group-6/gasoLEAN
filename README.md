# Welcome to your Expo app 👋

This is an [Expo](https://expo.dev) project created with [`create-expo-app`](https://www.npmjs.com/package/create-expo-app).

## Get started

1. Install dependencies

   ```bash
   npm install
   ```

2. Start the app

   ```bash
    npx expo start
   ```

In the output, you'll find options to open the app in a

- [development build](https://docs.expo.dev/develop/development-builds/introduction/)
- [Android emulator](https://docs.expo.dev/workflow/android-studio-emulator/)
- [iOS simulator](https://docs.expo.dev/workflow/ios-simulator/)
- [Expo Go](https://expo.dev/go), a limited sandbox for trying out app development with Expo

You can start developing by editing the files inside the **app** directory. This project uses [file-based routing](https://docs.expo.dev/router/introduction).

## Get a fresh project

When you're ready, run:

```bash
npm run reset-project
```

This command will move the starter code to the **app-example** directory and create a blank **app** directory where you can start developing.

## Learn more

To learn more about developing your project with Expo, look at the following resources:

- [Expo documentation](https://docs.expo.dev/): Learn fundamentals, or go into advanced topics with our [guides](https://docs.expo.dev/guides).
- [Learn Expo tutorial](https://docs.expo.dev/tutorial/introduction/): Follow a step-by-step tutorial where you'll create a project that runs on Android, iOS, and the web.

## Join the community

Join our community of developers creating universal apps.

- [Expo on GitHub](https://github.com/expo/expo): View our open source platform and contribute.
- [Discord community](https://chat.expo.dev): Chat with Expo users and ask questions.

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
```bash
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
```


### SETUP

```bash
git clone <your-repository-url>
cd backend

python3 -m venv myenv
source myenv/bin/activate

pip install -r app/requirements.txt

uvicorn app.main:app --reload

http://localhost:8000/docs      # Interactive API docs (Swagger UI)
http://localhost:8000/api/v1    # API base path
```

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

