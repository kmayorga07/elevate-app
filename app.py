import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Function to get coordinates from an address using OpenCage Geocoding API
def get_coordinates(address):
    geocoding_api_url = "https://api.opencagedata.com/geocode/v1/json"
    params = {
        'q': address,
        'key': '82e95f5d77cb415b8867f2e5cb1ec8ed'
    }
    response = requests.get(geocoding_api_url, params=params).json()
    if response['status']['code'] == 200 and len(response['results']) > 0:
        location = response['results'][0]['geometry']
        return location['lat'], location['lng']
    else:
        return None, None

# Function to get elevation using Open-Elevation API
def get_elevation(lat, lng):
    elevation_api_url = "https://api.open-elevation.com/api/v1/lookup"
    params = {
        'locations': f'{lat},{lng}'
    }
    response = requests.get(elevation_api_url, params=params).json()
    if 'results' in response and len(response['results']) > 0:
        elevation = response['results'][0]['elevation']
        return elevation * 3.28084  # Convert meters to feet
    else:
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_elevation', methods=['POST'])
def get_elevation_route():
    address = request.json['address']
    lat, lng = get_coordinates(address)
    if lat is None or lng is None:
        return jsonify({'error': 'Invalid address'}), 400

    elevation = get_elevation(lat, lng)
    if elevation is None:
        return jsonify({'error': 'Could not fetch elevation'}), 500

    return jsonify({'elevation': round(elevation, 2)})

if __name__ == "__main__":
    app.run(debug=True)
