import os
import json
from typing import List, Tuple, Dict
from parent_property import Property
from child_properties import House, Apartment
from amenity import Amenity
from ingestion import ingest_files
from score import *

def read_request(request_filename: str) -> Tuple[dict, dict]:
    """
    This method reads a request file in json format
    and returns two dictionaries; one containing the
    house_importance features and one containing the 
    amenity_importance features.
    """
    # TODO: Step 1 - Define this method to read a JSON request and return 2 dictionaries
    with open(request_filename, 'r') as file:
        request_data = json.load(file)
    house_importance = {}
    amenity_accessibility = {}

    house_request = request_data.get("request", {}).get("house_importance", {})
    house_importance["suburb"] = house_request.get("suburb")
    house_importance["prop_type"] = house_request.get("prop_type")
    house_importance["bedrooms"] = house_request.get("bedrooms")
    house_importance["bathrooms"] = house_request.get("bathrooms")
    house_importance["parking_spaces"] = house_request.get("parking_spaces")
    house_importance["price"] = house_request.get("price")
    house_importance["property_features"] = house_request.get("property_features")

    amenities_request = request_data.get("request", {}).get("amenities_accessibility", {})
    amenity_accessibility["train_station"] = amenities_request.get("train_station")
    amenity_accessibility["school"] = amenities_request.get("school", {})
    amenity_accessibility["medical_centre"] = amenities_request.get("medical_centre")
    amenity_accessibility["sport_facility"] = amenities_request.get("sport_facility", {})
    
    return house_importance, amenity_accessibility

house_importance, amenity_accessibility = read_request("request.json")
print("House Importance:", house_importance)
print("Amenity Accessibility:", amenity_accessibility)


def find_matching_properties(props: List[Property], house_importance: dict) -> List[Property]:
    """
    THis method recevied a list of all properties and a dictionary that
    contains the house importance criteria from a user's request 
    and returns a list of Property objects that match the user's request
    """
    # TODO: Step 2 - Define this method to return a list of matching properties
    matching_props = []
    for props_n in props:
        if house_importance.get("prop_type") == props_n.get_prop_type() or house_importance.get("prop_type") is None:
            if props_n.get_suburb() == house_importance.get("suburb") or house_importance.get("suburb") is None:
                if house_importance.get("property_features") in props_n.get_property_features() or house_importance.get("property_features") is None:
                    if house_importance.get("bedrooms") <= props_n.get_bedrooms() or house_importance.get("bedrooms") is None:
                        if house_importance.get("bathrooms") <= props_n.get_bathrooms() or house_importance.get("bathrooms") is None:
                            if house_importance.get("parking_spaces") <= props_n.get_parking_spaces() or house_importance.get("parking_spaces") is None:
                                if house_importance.get("price") >= props_n.get_price() or house_importance.get("price") is None:
                                    matching_props.append(props_n)
    return matching_props


def create_response_dict(scored_properties: dict) -> dict:
    """
    This method takes in a dictionary that has the property objects 
    and their star scores and creates a dictionary in JSON format 
    that can be written into a file
    """
    # TODO: Step 3 - Define this method to create a response dictionary
    response_dict = {"properties": []}
    for star_score, prop_object in scored_properties.items():
        property_dict = {"property_id": prop_object.get_prop_id(), "star_score": float(star_score)}
        response_dict["properties"].append(property_dict)

    return response_dict

def produce_star_scores(request_filename: str, properties_file: str, amenities_files: List[str]) -> dict:
    # Read the properties and amenities
    medical_file, schools_file, train_stations, sport_facilities = amenities_files
    props, amenities = ingest_files(properties_file, medical_file, schools_file, train_stations, sport_facilities)

    # Read the request and get the dictionaries of house_importance and amenity_accessibility
    house_importance, amenity_accessibility = read_request(request_filename)

    # Collect properties that match the property criteria
    matched_props = find_matching_properties(props, house_importance)

    # Score properties using the amenity amenity_accessibility dictionary
    prop_scores = [score_property(x, amenities, amenity_accessibility) for x in matched_props]

    # Now, we can normalise the scores that we just got
    norm_scores = normalise_scores(prop_scores)

    # Create a collection matching property object to Score
    prop_scored = dict(zip(norm_scores, matched_props))

    # Create a response dictionary
    response_dict = create_response_dict(prop_scored)
    
    # Return the response dictionary from step 3 and the list of matching property family objects
    return response_dict, matched_props

def respond(response_dict: dict) -> None:
    """
    This function reads a response dictionary and creates a JSON 
    file based on the content of the response dictionary
    """
    # TODO: Step 4 - Create this method to read a response dictionary
    # and create a JSON file
    properties = response_dict["properties"]
    sorted_prop = sorted(properties, key=lambda x:x["star_score"] , reverse=True)
    response_dict["properties"] = sorted_prop
    with open("response.json", "w") as file:
        json.dump(response_dict, file)
        file.write("\n")

if __name__ == '__main__':
    response_dict, matched_props = produce_star_scores('request.json', 'melbourne_properties.csv', ['melbourne_medical.csv', 'melbourne_schools.csv', 'train_stations.csv', 'sport_facilities.csv'])
    print(f"{len(matched_props)} properties matched with the user's request")
    respond(response_dict)
    # Check if response.json exists in the current directory
    if os.path.exists("/home/response.json"):
        print("File created successfully")
    else:
        print("File not created. Some Error occurred")
