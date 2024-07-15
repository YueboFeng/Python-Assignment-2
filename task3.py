def process_schools(file_name: str) -> dict:
    """ This method is to store information of schools. """
    school_dict = {}
    
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
                    school_lat, school_lon = lat_lon_list[0], lat_lon_list[1]
                else:
                    school_lat, school_lon = lat_lon_list[1], lat_lon_list[0]
            else:
                school_lat, school_lon = None, None
            
            school_sub_dict = {
                "school_no": fields[0].strip(),
                "school_name": fields[1].strip(),
                "school_type": fields[2].strip(),
                "school_lat": school_lat,
                "school_lon": school_lon
            }
            school_dict[fields[0]] = school_sub_dict
    
    return school_dict


def process_medicals(file_name: str) -> dict:
    """ This method is to store information of medicals. """
    medical_dict = {}
    
    with open (file_name) as f:
        header = f.readline().strip().split(",")
        for fields in f:
            fields = fields.strip().split(",")
            medical_sub_dict = {
                "gp_code": fields[0].strip(),
                "gp_name": fields[1].strip(),
                "location": (fields[-2] + ", "+ fields[-1]).strip(),
                "gp_lat": float(fields[-2][10:].replace(":", "").replace("}", "").replace("\"", ""))
                    if fields[-2][10:] else None,
                "gp_lon": float(fields[-1][9:].replace(":", "").replace("}", "").replace("\"", ""))
                    if fields[-1][9:] else None
            }
            medical_dict[fields[0].strip()] = medical_sub_dict
    
    return medical_dict


def process_sport(file_name: str) -> dict:
    """ This method is to store information of facilities. """
    sport_dict = {}
    
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
                    sport_lat, sport_lon = lat_lon_list[0], lat_lon_list[1]
                else:
                    sport_lat, sport_lon = lat_lon_list[1], lat_lon_list[0]
            else:
                sport_lat, sport_lon = None, None

            sport_sub_dict = {
                "facility_id": fields[0].strip(),
                "facility_name": fields[2].strip(),
                "sport_lat": float(fields[3].strip()),
                "sport_lon": float(fields[4].strip()),
                "sport_played": fields[5].strip()
            }
            sport_dict[fields[0]] = sport_sub_dict
    
    return sport_dict


def main():
    """ This is the main entry point of the script. """
    school_dict = process_schools('sample_melbourne_schools.csv')
    medical_dict = process_medicals('sample_melbourne_medical.csv')
    sport_dict = process_sport('sample_sport_facilities.csv')

    sample_medical_code = 'mgp0041'
    print(f"There are {len(school_dict)} schools and {len(sport_dict)} sport facilities in our dataset")
    print(f"The location for {medical_dict[sample_medical_code]['gp_name']} is {medical_dict[sample_medical_code]['gp_lat']}, {medical_dict[sample_medical_code]['gp_lon']}")

if __name__ == '__main__':
    main()
