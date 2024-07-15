def extract_information(property_string: str) -> dict:
    """ This method is to store information of properties. """
    fields = property_string.split(",")
    property_dict = {
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
    
    return property_dict


def add_feature(property_dict: dict, feature: str) -> None:
    """ This method is add features to properties information. """
    if feature not in property_dict["property_features"]:
        property_dict["property_features"].append(feature)

def remove_feature(property_dict: dict, feature: str) -> None:
    """ This method is to remove features from properties information. """
    if feature in property_dict["property_features"]:
        property_dict["property_features"].remove(feature)

def main():
    """ This is the main entry point of the script. """
    sample_string = "P10001,3 Antrim Place Langwarrin VIC 3910,4,2,2,-38.16655678,145.1838435,,608,257,870000,dishwasher;central heating"
    property_dict = extract_information(sample_string)
    print(f"The first property is at {property_dict['full_address']} and is valued at ${property_dict['price']}")

    sample_string_2 = "P10002,G01/7 Rugby Road Hughesdale VIC 3166,2,1,1,-37.89342337,145.0862616,1,,125,645000,dishwasher;air conditioning;balcony"
    property_dict_2 = extract_information(sample_string_2)

    print(f"The second property is in {property_dict_2['suburb']} and is located on floor {property_dict_2['floor_number']}")

    add_feature(property_dict, 'electric hot water')
    print(f"Property {property_dict['prop_id']} has the following features: {property_dict['property_features']}")

if __name__ == '__main__':
    main()
