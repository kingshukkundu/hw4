import unittest
import requests
import json
import time

# Base API URL
API_URL = "https://hw4-indol.vercel.app/county_data"

# Valid test case
VALID_PAYLOAD = {
    "zip": "02138",
    "measure_name": "Adult obesity"
}

# Invalid measure name
INVALID_MEASURE_PAYLOAD = {
    "zip": "02138",
    "measure_name": "Invalid Measure"
}

# Invalid ZIP code
INVALID_ZIP_PAYLOAD = {
    "zip": "99999",
    "measure_name": "Adult obesity"
}

# Missing parameters
MISSING_PARAM_PAYLOAD = {
    "zip": "02138"
}

# Easter egg (coffee=teapot)
TEAPOT_PAYLOAD = {
    "zip": "02138",
    "measure_name": "Adult obesity",
    "coffee": "teapot"
}

class TestCountyDataAPI(unittest.TestCase):

    def log_response(self, response, test_name, payload=None):
        """Log details of the API response"""
        print("\n========================================")
        print(f"🔹 TEST CASE: {test_name}")
        print(f"🔹 Request Payload: {json.dumps(payload, indent=2)}") if payload else None
        print(f"🔹 URL: {response.url}")
        print(f"🔹 HTTP Status Code: {response.status_code}")
        print(f"🔹 Response Headers: {response.headers}")
        try:
            response_json = response.json()
            print(f"🔹 Response JSON: {json.dumps(response_json, indent=2)}")
        except json.JSONDecodeError:
            print(f"🔹 Response Text: {response.text}")
        print("========================================\n")

    def test_valid_request(self):
        """Test if a valid request returns a 200 OK response with JSON data"""
        start_time = time.time()
        response = requests.post(API_URL, json=VALID_PAYLOAD)
        elapsed_time = time.time() - start_time

        self.log_response(response, "Valid Request", VALID_PAYLOAD)
        self.assertEqual(response.status_code, 200, "Valid request should return 200 OK")
        self.assertTrue(response.headers["Content-Type"].startswith("application/json"))
        self.assertIsInstance(response.json(), list, "Response should be a JSON list")

        print(f"✅ Test passed in {elapsed_time:.4f} seconds.\n")

    def test_missing_parameters(self):
        """Test if missing parameters return a 400 Bad Request"""
        start_time = time.time()
        response = requests.post(API_URL, json=MISSING_PARAM_PAYLOAD)
        elapsed_time = time.time() - start_time

        self.log_response(response, "Missing Parameters", MISSING_PARAM_PAYLOAD)
        self.assertEqual(response.status_code, 400, "Missing parameters should return 400 Bad Request")

        print(f"✅ Test passed in {elapsed_time:.4f} seconds.\n")

    def test_invalid_measure_name(self):
        """Test if an invalid measure name returns a 404 Not Found"""
        start_time = time.time()
        response = requests.post(API_URL, json=INVALID_MEASURE_PAYLOAD)
        elapsed_time = time.time() - start_time

        self.log_response(response, "Invalid Measure Name", INVALID_MEASURE_PAYLOAD)
        self.assertEqual(response.status_code, 404, "Invalid measure name should return 404 Not Found")

        print(f"✅ Test passed in {elapsed_time:.4f} seconds.\n")

    def test_invalid_zip_code(self):
        """Test if an invalid ZIP code returns a 404 Not Found"""
        start_time = time.time()
        response = requests.post(API_URL, json=INVALID_ZIP_PAYLOAD)
        elapsed_time = time.time() - start_time

        self.log_response(response, "Invalid ZIP Code", INVALID_ZIP_PAYLOAD)
        self.assertEqual(response.status_code, 404, "Invalid ZIP code should return 404 Not Found")

        print(f"✅ Test passed in {elapsed_time:.4f} seconds.\n")

    def test_teapot_easter_egg(self):
        """Test if passing coffee=teapot returns 418 I'm a Teapot"""
        start_time = time.time()
        response = requests.post(API_URL, json=TEAPOT_PAYLOAD)
        elapsed_time = time.time() - start_time

        self.log_response(response, "Teapot Easter Egg", TEAPOT_PAYLOAD)
        self.assertEqual(response.status_code, 418, "Passing coffee=teapot should return 418 I'm a Teapot")

        print(f"✅ Test passed in {elapsed_time:.4f} seconds.\n")

    def test_non_existent_endpoint(self):
        """Test if calling a non-existent endpoint returns a 404 Not Found"""
        start_time = time.time()
        response = requests.post("https://hw4-indol.vercel.app/non_existent")
        elapsed_time = time.time() - start_time

        self.log_response(response, "Non-Existent Endpoint")
        self.assertEqual(response.status_code, 404, "Non-existent endpoint should return 404 Not Found")

        print(f"✅ Test passed in {elapsed_time:.4f} seconds.\n")

if __name__ == "__main__":
    unittest.main()
