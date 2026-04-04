from pydantic import BaseModel
from typing import Optional


class Property(BaseModel):
    title: str
    location: str
    price: str
    property_type: str
    bedrooms: str
    bathrooms: Optional[int]
    area: Optional[str]
    link: str
    

property_data = {
    "title": "Spacious 2 Bedroom Apartment in Downtown",
    "location": "New York",
    "price": "$500,000",
    "property_type": "Apartment",
    "bedrooms": "2",
    "bathrooms": "2",
    "area": None,
    "link": "https://example.com/apartment"
}

property = Property(
    title=property_data["title"],
    location=property_data["location"],
    price=property_data["price"],
    property_type=property_data["property_type"],
    bedrooms=property_data["bedrooms"],
    bathrooms=property_data["bathrooms"],
    area=property_data["area"],
    link=property_data["link"]
)

print(property)