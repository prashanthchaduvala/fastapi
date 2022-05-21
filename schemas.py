from pydantic import BaseModel

# Create Address Schema (Pydantic Model)
class AddressDoCreate(BaseModel):
    country: str
    city: str
    location: str
    zip_code: int
    latitude: str
    longitude: str

# Complete Address Schema (Pydantic Model)
class Address(BaseModel):
    id: int
    country: str
    city: str
    location: str
    zip_code: int
    latitude: str
    longitude: str

    class Config:
        orm_mode = True