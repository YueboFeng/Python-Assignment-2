from haversine import haversine_distance

def process_properties(file_name: str) -> dict:
    """ The method is to store information of properties. """
    property_dict = {}
    
    with open (file_name) as f:
        header = f.readline().strip().split(",")
        
        for fields in f:
            fields = fields.strip().split(",")
            value_list = []
            lat_lon_list = []
            
            # Extract all values that can be converted to float.
            for field in fields:
                try:
                    value = float(field)
                    value_list.append(value)
                except	ValueError:
                    pass

            # Extract latitude and longitude values.
            for value in value_list:
                decimal_part = str(value).split(".")[1]
                if len(decimal_part) > 1:
                    lat_lon_list.append(value)

            # Initialize valid latitude and longitude values.
            if len(lat_lon_list) == 2:
                if lat_lon_list[0] < 0:
                    latitude, longitude = lat_lon_list[0], lat_lon_list[1]
                else:
                    latitude, longitude = lat_lon_list[1], lat_lon_list[0]
            else:
                latitude, longitude = None, None
            
            property_sub_dict = {
                "prop_id": fields[0].strip(),
                "prop_type": "apartment" if "/" in fields[1].strip() else "house",
                "full_address": fields[1].strip(),
                "suburb": fields[1].strip().split(" ")[3],
                "bedrooms": int(fields[2].strip()),
                "bathrooms": int(fields[3].strip()),
                "parking_spaces": int(fields[4].strip()),
                "latitude": float(fields[5].strip()),
                "longitude": float(fields[6].strip()),
                "floor_number": int(fields[7].strip()) if fields[7].strip() else None,
                "land_area": int(fields[8].strip()) if fields[8].strip() else None,
                "floor_area": int(fields[9].strip()),
                "price": int(fields[10].strip()),
                "property_features": fields[11].strip().split(";") if fields[11].strip() else None
            }
            property_dict[fields[0].strip()] = property_sub_dict

    return property_dict

def process_stations(file_name: str) -> dict:
    """ This method is to store information of stations. """
    stop_dict = {}
    
    with open (file_name) as f:
        header = f.readline().strip().split(",")
        
        for fields in f:
            fields = fields.strip().split(",")
            value_list = []
            lat_lon_list = []
            
            # Extract all values that can be converted to float
            for field in fields:
                try:
                    value = float(field)
                    value_list.append(value)
                except	ValueError:
                    pass

            # Extract latitude and longitude values.
            for value in value_list:
                decimal_part = str(value).split(".")[1]
                if len(decimal_part) > 1:
                    lat_lon_list.append(value)

            # Initialize valid latitude and longitude values.
            if len(lat_lon_list) == 2:
                if lat_lon_list[0] < 0:
                    stop_lat, stop_lon = lat_lon_list[0], lat_lon_list[1]
                else:
                    stop_lat, stop_lon = lat_lon_list[1], lat_lon_list[0]
            else:
                stop_lat, stop_lon = None, None
            
            stop_sub_dict = {
                "stop_id": fields[0].strip(),
                "stop_name": fields[1].strip(),
                "stop_lat": fields[2].strip(),
                "stop_lon": fields[3].strip()
            }
            stop_dict[fields[0].strip()] = stop_sub_dict

    return stop_dict

def nearest_station(properties: dict, stations: dict, prop_id: str) -> str:
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    info = properties[prop_id]
    prop_lat = float(info["latitude"])
    prop_lon = float(info["longitude"])
    station_list = list(stations.values())
    distance_list = []
    
    for station in station_list:
        stop_lat = float(station["stop_lat"])
        stop_lon = float(station["stop_lon"])
        distance = haversine_distance(prop_lat, prop_lon, stop_lat, stop_lon)
        distance_list.append(distance)
    
    nearest_distance = min(distance_list)
    nearest_station = station_list[distance_list.index(nearest_distance)]
    
    return nearest_station["stop_name"]

def main():
    """
    You need not touch this function, if your 
    code is correct, this function will work as intended 
    """
    # Process the properties
    properties_file = 'sample_properties.csv'
    properties = process_properties(properties_file)

    # Process the train stations
    stations_file = 'train_stations.csv'
    stations = process_stations(stations_file)

    # Check the validity of stations
    sample_prop = 'P10001'
    print(f"The nearest station for property {sample_prop} is {nearest_station(properties, stations, sample_prop)}")
    


if __name__ == '__main__':
    main()
