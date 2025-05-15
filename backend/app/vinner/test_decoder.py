from vinner.decoder import decode_vin

def test_sample_vin():
    vin = "1HGCM82633A004352"
    result = decode_vin(vin)
    assert "Make" in result
    assert result["Make"].upper() == "HONDA"
    print("Test Passed. Vehicle Info:", result)

if __name__ == "__main__":
    test_sample_vin()

