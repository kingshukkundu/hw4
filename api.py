import sqlite3
from flask import Flask, request, jsonify, abort

app = Flask(__name__)

# For demonstration, list of valid measure names:
VALID_MEASURES = {
    "Violent crime rate",
    "Unemployment",
    "Children in poverty",
    "Diabetic screening",
    "Mammography screening",
    "Preventable hospital stays",
    "Uninsured",
    "Sexually transmitted infections",
    "Physical inactivity",
    "Adult obesity",
    "Premature Death",
    "Daily fine particulate matter"
}

DATABASE = "data.db"  # Adjust path if needed

def get_db_connection():
    """Return a new SQLite DB connection."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # So we can get dict-like row objects
    return conn

@app.route('/county_data', methods=['POST'])
def county_data():
    # 1. Check if JSON body is present
    if not request.is_json:
        abort(400, description="Request body must be JSON.")

    # 2. Parse JSON
    data = request.get_json()

    # 3. Check the special "coffee=teapot" key => 418
    if data.get("coffee") == "teapot":
        abort(418)

    # 4. Check required parameters: "zip" and "measure_name"
    zip_code = data.get("zip")
    measure_name = data.get("measure_name")

    if not zip_code or not measure_name:
        # Missing required fields => 400
        abort(400, description="Both 'zip' and 'measure_name' must be provided.")

    # 5. Validate measure_name is known
    if measure_name not in VALID_MEASURES:
        # Not a valid measure => 404
        abort(404, description="Measure name not found in the database list.")

    # 6. Query the database
    conn = get_db_connection()
    cursor = conn.cursor()

    # Example join:
    #   - We join on county + state_abbreviation from zip_county
    #     matching county + state in county_health_rankings
    #   - Filter by the provided zip code and measure_name
    sql = """
    SELECT 
        chr.county,
        chr.state,
        chr.state_code,
        chr.county_code,
        chr.year_span,
        chr.measure_name,
        chr.measure_id,
        chr.numerator,
        chr.denominator,
        chr.raw_value,
        chr.confidence_interval_lower_bound,
        chr.confidence_interval_upper_bound,
        chr.data_release_year,
        chr.fipscode
    FROM county_health_rankings chr
    JOIN zip_county zc
        ON chr.county = zc.county
        AND chr.state = zc.state_abbreviation
    WHERE zc.zip = ?
      AND chr.measure_name = ?
    """

    cursor.execute(sql, (zip_code, measure_name))
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        # If no matching rows => 404
        abort(404, description="No matching data found for that zip and measure_name.")

    # 7. Convert results to a list of dict
    results = []
    for row in rows:
        # row is an sqlite3.Row, so we can use dict-like access
        results.append({
            "confidence_interval_lower_bound": row["confidence_interval_lower_bound"],
            "confidence_interval_upper_bound": row["confidence_interval_upper_bound"],
            "county": row["county"],
            "county_code": row["county_code"],
            "data_release_year": row["data_release_year"],
            "denominator": row["denominator"],
            "fipscode": row["fipscode"],
            "measure_id": row["measure_id"],
            "measure_name": row["measure_name"],
            "numerator": row["numerator"],
            "raw_value": row["raw_value"],
            "state": row["state"],
            "state_code": row["state_code"],
            "year_span": row["year_span"]
        })

    return jsonify(results), 200

# A catch-all for any other endpoint => 404
@app.errorhandler(404)
def not_found(e):
    return jsonify(error=str(e)), 404

# Example: handle 400 explicitly
@app.errorhandler(400)
def bad_request(e):
    return jsonify(error=str(e)), 400

# Example: handle 418 (I'm a Teapot)
@app.errorhandler(418)
def teapot(e):
    return jsonify(error=str(e)), 418

if __name__ == '__main__':
    # Run locally for testing
    # On Vercel or other platforms, you typically won't call app.run() directly.
    app.run(debug=True, host='0.0.0.0', port=5000)
