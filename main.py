import requests
from flask import Flask, render_template, request
from geopy.geocoders import Nominatim

app = Flask(__name__)

# Function to generate motorcycle route based on user preferences
def generate_motorcycle_route(start_address, end_address, road_type, twistiness, trip_type, length):
    # Geocode starting and ending addresses to get coordinates
    geolocator = Nominatim(user_agent="motorcycle_route_planner")
    start_location = geolocator.geocode(start_address)
    
    if start_location is None:
        print("Error: Unable to geocode the starting address")
        return None
    
    if trip_type == "point_to_point":
        end_location = geolocator.geocode(end_address)
        if end_location is None:
            print("Error: Unable to geocode the ending address")
            return None
    
    # Construct the bounding box for the API call based on the starting location
    bbox = get_bounding_box(start_location.latitude, start_location.longitude)
    
    # Query OpenStreetMap API to retrieve road data based on user preferences and bounding box
    url = f'https://api.openstreetmap.org/api/0.6/map?bbox={bbox}'
    response = requests.get(url)
    
    if response.status_code == 200:
        # Parse road data from the response
        road_data = parse_road_data(response.json(), road_type, twistiness)
        
        # Perform routing based on the retrieved road data
        route = calculate_route(road_data, trip_type, length)
        
        return route
    else:
        print("Error: Unable to retrieve road data from OpenStreetMap API")
        return None

# Function to parse road data from the API response
def parse_road_data(data, road_type, twistiness):
    # Parse road data from the API response based on user preferences
    # You would filter the data based on road type and twistiness level
    # and convert it into a format suitable for routing
    
    # For demonstration purposes, let's assume we're parsing all roads within the bounding box
    road_data = []
    for way in data['elements']:
        if 'highway' in way['tags']:  # Check if the element represents a road
            road_data.append({
                'type': way['tags']['highway'],  # Road type
                'coordinates': [(node['lon'], node['lat']) for node in way['nodes']]  # Coordinates of the road
            })
    
    return road_data

# Function to calculate route based on road data and user preferences
def calculate_route(road_data, trip_type, length):
    # Perform routing based on road data and user preferences
    # This could involve using a routing algorithm like Dijkstra's algorithm
    # to find the shortest path considering road type and twistiness level
    
    # For demonstration purposes, let's assume we're generating a route using the first road in the data
    if road_data:
        return road_data[0]['coordinates']  # Return the coordinates of the first road
    else:
        return None

# Function to get the bounding box for the API call based on the starting location
def get_bounding_box(lat, lon):
    # Adjust the bounding box size as needed
    bbox = f"{lon - 0.01},{lat - 0.01},{lon + 0.01},{lat + 0.01}"
    return bbox

# Define routes
@app.route('/')
def index():
    trip_type = request.args.get('trip_type', 'round_trip')
    return render_template('index.html', trip_type=trip_type)

@app.route('/generate_route', methods=['POST'])
def generate_route():
    # Retrieve user preferences and locations from the form
    start_address = request.form['start_address']
    end_address = request.form.get('end_address', None)
    road_type = request.form['road_type']
    twistiness = request.form['twistiness']
    trip_type = request.form['trip_type']
    length = float(request.form['length'])  # Convert length to float
    
    # Call routing algorithm function with user preferences
    route = generate_motorcycle_route(start_address, end_address, road_type, twistiness, trip_type, length)
    
    # Render template with route information
    return render_template('route.html', route=route)

if __name__ == '__main__':
    app.run(debug=True)
