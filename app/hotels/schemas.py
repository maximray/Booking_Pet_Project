from pydantic import BaseModel


class SGetHotels(BaseModel):
    id : int
    name : str
    location : str
    services : list[str]
    rooms_quantity : int
    image_id : int
    rooms_left : int



class SGetSpecificHotel(BaseModel):
    
    class SGetSpecificHotel1(BaseModel):
        id : int
        name : str
        location : str
        services : list[str]
        rooms_quantity : int
        image_id : int
    
    Hotels : SGetSpecificHotel1