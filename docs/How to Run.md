# Clone the Repo Locally

## Backend

1. Clone the repository locally.
2. Copy and paste the cloned folder. This is for the backend.

### Required Software
- Python 3.12 or higher
- npm
- Git

## Frontend

1. Ensure the frontend is already in the main branch.
2. Run **`npm install`** from the base of the folder.
3. Run **`npx expo start --clear`**.

## Backend

1. Navigate into the copy of the backend folder that we created earlier.
2. Run the following commands in the specified order:
   a. `git checkout backend`
   b. `cd backend`
   c. `python -m venv venv`
   d. `source ./venv/bin/activate`
   e. `./venv/bin/pip install -r app/requirements.txt`
   f. `./venv/bin/python app/main.py`
3. The backend should be up and running now.

## App

When you start the frontend, it should produce a QR code on the terminal.

1. Install the Expo Go application on your phone.
2. Open the Expo Go application and click on "Scan QR Code".
3. The app should open up and be ready to go.
