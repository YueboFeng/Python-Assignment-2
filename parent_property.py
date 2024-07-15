# parent_property
from abc import ABC, abstractmethod
from typing import Tuple, List, Union
import math
from amenity import Amenity

class Property(ABC):
    """ This class is to store information of properties. """
    def __init__(self, prop_id: str, 
                        bedrooms: int, 
                        bathrooms: int, 
                        parking_spaces: int, 
                        full_address: str,
                        floor_area: int,
                        price: int,
                        property_features: List[str],
                        coordinates: Tuple[float, float]):
        self.prop_id = prop_id
        self.full_address = full_address
        self.coordinates = coordinates
        self.suburb = full_address.split(" ")[3]
        self.prop_type = self.prop_type
        self.bedrooms = bedrooms
        self.bathrooms = bathrooms
        self.parking_spaces = parking_spaces
        self.floor_area = floor_area
        self.price = price
        self.property_features = property_features
    
    def get_prop_id(self) -> str:
        return self.prop_id

    def get_full_address(self) -> str:
        return self.full_address

    def get_suburb(self) -> str:
        return self.suburb
    
    @abstractmethod
    def get_prop_type(self) -> str:
        pass   
    
    def set_bedrooms(self, bedrooms: int) -> None:
        self.bedrooms = bedrooms
    
    def get_bedrooms(self) -> int:
        return self.bedrooms
    
    def set_bathrooms(self, bathrooms: int) -> None:
        self.bathrooms = bathrooms
    
    def get_bathrooms(self) -> int:
        return self.bathrooms
    
    def set_parking_spaces(self, parking_spaces: int) -> None:
        self.parking_spaces = parking_spaces

    def get_parking_spaces(self) -> int:
        return self.parking_spaces
    
    def get_coordinates(self) -> Tuple[float, float]:
        return self.coordinates

    @abstractmethod
    def set_floor_number(self, floor_number: int) -> None:
        pass

    @abstractmethod
    def get_floor_number(self) -> Union[int,None]:
        pass
    
    @abstractmethod
    def set_land_area(self, land_area: int) -> None:
        pass

    @abstractmethod
    def get_land_area(self) -> Union[int,None]:
        pass
    
    def set_floor_area(self, floor_area: int) -> None:
        self.floor_area = floor_area
    
    def get_floor_area(self) -> int:
        return self.floor_area

    def set_price(self, price: int) -> None:
        self.price = price
    
    def get_price(self) -> int:
        return self.price
    
    def set_property_features(self, property_features: List[str]) -> None:
        self.property_features = property_features
    
    def get_property_features(self) -> List[str]:
        return self.property_features

    def add_feature(self, feature: str) -> None:
        if feature not in self.property_features:
            self.property_features.append(feature)
        
    def remove_feature(self, feature: str) -> None:
        if feature in self.property_features:
            self.property_features.remove(feature)

    def amenity_filter(self, amenities: List[Amenity], amenity_type: str, amenity_subtype: str = None) -> List[Amenity]:
        amenities_filter = []
        amenities_filter_all = []
        
        for amenity_n in amenities: 
            if amenity_n.get_amenity_type() == amenity_type:
                amenities_filter_all.append(amenity_n)
                if amenity_n.get_amenity_subtype() == amenity_subtype:
                    amenities_filter.append(amenity_n)
                if amenity_n.get_amenity_subtype() == 'Pri/Sec':
                    amenities_filter.append(amenity_n)
                if amenity_subtype is None:
                    amenities_filter = amenities_filter_all
                    
        return amenities_filter

    def nearest_amenity(self, amenities: List[Amenity], amenity_type: str, amenity_subtype: str = None) -> Tuple[Amenity, float]:
        nearest_amenity = None
        min_distance = float('inf')
        pro_lat = self.coordinates[0]
        pro_lon = self.coordinates[1]
        amenities = self.amenity_filter(amenities, amenity_type, amenity_subtype)
        
        for amenity_n in amenities:
                coordinate = amenity_n.coordinates
                Amenity_lat = coordinate[0]
                Amenity_lon = coordinate[1]
                distance = self.haversine_distance(pro_lat, pro_lon, Amenity_lat, Amenity_lon)
                if distance < min_distance:
                    min_distance = distance
                    nearest_amenity = amenity_n

        return (nearest_amenity, min_distance)

    def haversine_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        radius_of_earth = 6371  # Radius of the earth in kilometers.
        distance = radius_of_earth * c
        
        return distance

if __name__ == '__main__':
    pass
