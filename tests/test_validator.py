import os
import json
import unittest
import requests
import logging


class TestSTACValidator(unittest.TestCase):
    def setUp(self):
        self.url = "http://localhost:7000/"
        self.test_data_dir = "stac_json_samples"

    def test_stac_validator(self):
        responses = []
        # Iterate through the files and store responses
        for filename in os.listdir(self.test_data_dir):
            if filename.endswith(".json"):
                file_path = os.path.join(self.test_data_dir, filename)
                with open(file_path, "r") as file:
                    stac_json = json.load(file)
                    response = requests.post(self.url, json=stac_json)
                    responses.append((filename, response))

        # Check all responses
        for filename, response in responses:
            try:
                print(f"{filename}: {response.json()}")
                self.assertEqual(
                    response.status_code, 200, f"Failed for file: {filename}"
                )
            except AssertionError as e:
                logging.error(f"{filename}: {e}")

        # Final log statement indicating that testing has finished
        logging.info("Finished testing STAC Validator.")


if __name__ == "__main__":
    unittest.main()
