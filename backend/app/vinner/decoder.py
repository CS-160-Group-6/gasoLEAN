import requests

class VINDecoderError(Exception):
    pass

def decode_vin(vin: str) -> dict:
    url = f"https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVin/{vin}?format=json"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        raise VINDecoderError(f"NHTSA API request failed: {str(e)}")

    data = response.json()
    results = data.get("Results", [])

    vehicle_info = {}
    for item in results:
        label = item.get("Variable")
        value = item.get("Value")
        if label in ["Make", "Model", "Model Year", "Vehicle Type"]:
            vehicle_info[label] = value or "N/A"

    if not vehicle_info:
        raise VINDecoderError("VIN decoding failed or returned no useful information.")

    return vehicle_info

