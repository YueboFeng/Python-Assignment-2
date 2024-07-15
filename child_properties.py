# Copy and paste your code from the previous task
from typing import Tuple, List, Union
import math
from amenity import Amenity
from parent_property import Property

class House(Property):
    """ This class is to store information of House properties. """
    def __init__(self, prop_id: str, 
                        bedrooms: int, 
                        bathrooms: int, 
                        parking_spaces: int, 
                        full_address: str,
                        land_area: int,
                        floor_area: int,
                        price: int,
                        property_features: List[str],
                        coordinates: Tuple[float, float]):
        self.prop_id = prop_id
        self.bedrooms = bedrooms
        self.bathrooms = bathrooms
        self.parking_spaces = parking_spaces
        self.full_address = full_address
        self.land_area = land_area
        self.floor_area = floor_area
        self.price = price
        self.property_features = property_features
        self.coordinates = coordinates
        self.suburb = full_address.split(" ")[3]
    
    def get_prop_type(self) -> str:
        return 'house'

    def get_land_area(self) -> Union[int,None]:
        return self.land_area

    def set_land_area(self, land_area: int) -> None:
        self.land_area = land_area

    def get_floor_number(self) -> int:
        return None
    
    def set_floor_number(self, floor_number: int) -> None:
        None

class Apartment(Property):
    """ This class is to store information of Apartment properties. """
    def __init__(self, prop_id: str, 
                        bedrooms: int, 
                        bathrooms: int, 
                        parking_spaces: int, 
                        full_address: str,
                        floor_number: int,
                        floor_area: int,
                        price: int,
                        property_features: List[str],
                        coordinates: Tuple[float, float]):
        self.prop_id = prop_id
        self.bedrooms = bedrooms
        self.bathrooms = bathrooms
        self.parking_spaces = parking_spaces
        self.full_address = full_address
        self.floor_number = floor_number
        self.floor_area = floor_area
        self.price = price
        self.property_features = property_features
        self.coordinates = coordinates
        self.suburb = full_address.split(" ")[3]
    
    def get_prop_type(self) -> str:
        return 'apartment'

    def get_floor_number(self) -> int:
        return self.floor_number
    
    def set_floor_number(self, floor_number: int) -> None:
        self.floor_number = floor_number

    def get_land_area(self) -> Union[int,None]:
        return None

    def set_land_area(self, land_area: int) -> None:
        None

if __name__ == '__main__':
    pass
