"""A Flask API for validating STAC (SpatioTemporal Asset Catalog) items using stac-check.

This API exposes an endpoint that accepts a JSON payload representing a STAC item,
validates it using stac-check, and returns validation results in the response.
"""

from flask import Flask, request, jsonify
from stac_check.lint import Linter
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)


@app.route("/", methods=["POST"])
def validate():
    """Validate a STAC item.

    This endpoint accepts a JSON payload representing a STAC item, validates it using
    stac-check, and returns validation results in the response. If the STAC item is
    valid, a 200 status code is returned. If the STAC item is invalid, a 400 status
    code is returned along with details about the issues. If there's an error in
    processing, a 500 status code is returned with the error message.

    :return: JSON response containing validation results
    """
    logging.info("Validating STAC")
    data = request.get_json()

    try:
        # Using stac_check to validate
        linter = Linter(data, assets=True)
        best_practices = linter.create_best_practices_dict()

        # Determine if there are any issues
        issues = [v for k, v in best_practices.items() if v]

        if issues:
            return (
                jsonify(
                    {
                        "status": "error",
                        "message": "STAC validation failed",
                        "issues": issues,
                    }
                ),
                400,
            )
        else:
            return jsonify({"status": "success", "message": "Valid STAC"}), 200

    except Exception as e:
        logging.error(f"Error during validation: {str(e)}")
        return (
            jsonify({"status": "error", "message": str(e), "error_type": str(type(e))}),
            500,
        )


if __name__ == "__main__":
    """Run the Flask application if the script is executed as the main module.

    Starts the Flask development server on http://localhost:7000.
    """
    app.run(debug=True, host="localhost", port=7000)
