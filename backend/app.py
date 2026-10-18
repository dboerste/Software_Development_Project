
import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

# Initialize Flask
app = Flask(__name__)

# Allow frontend to communicate with backend
CORS(app, resources={
    r"/api/*": {"origins": "http://localhost:8081"}
})

# Retrieve API key from environment
TICKETMASTER_API_KEY = os.getenv("TICKETMASTER_API_KEY")

# Ticketmaster API endpoint
TICKETMASTER_URL = "https://app.ticketmaster.com/discovery/v2/events.json"


# Test backend connection
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "GitLost backend is running!"})


# Retrieve events from Ticketmaster
@app.route("/api/events", methods=["GET"])
def get_events():

    # Verify API key exists
    if not TICKETMASTER_API_KEY:
        return jsonify({"error": "API key not configured"}), 500

    # Get search parameters from frontend
    city = request.args.get("city", "").strip()
    event_type = request.args.get("type", "all")

    # Require a city
    if not city:
        return jsonify({"error": "Please enter a city"}), 400

    # Ticketmaster request parameters
    params = {
        "apikey": TICKETMASTER_API_KEY,
        "city": city,
        "size": 20,
        "sort": "date,asc"
    }

    # Map frontend categories to Ticketmaster classifications
    categories = {
        "concerts": "Music",
        "sports": "Sports",
        "arts": "Arts & Theatre"
    }

    if event_type in categories:
        params["classificationName"] = categories[event_type]

    try:
        # Request events from Ticketmaster
        response = requests.get(
            TICKETMASTER_URL,
            params=params,
            timeout=10
        )

        response.raise_for_status()

        # Convert response to JSON
        data = response.json()

        # Extract event list
        events = data.get("_embedded", {}).get("events", [])

        # Return events to frontend
        return jsonify(events)

    except requests.exceptions.RequestException as error:
        print(f"Ticketmaster API error: {error}")

        return jsonify({
            "error": "Failed to retrieve events"
        }), 502


# Start Flask server
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
