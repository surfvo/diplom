import datetime

from pydantic import BaseModel
from typing import Optional


class ParkingPlaceBase(BaseModel):
    id: Optional[int]
    owner_id: Optional[int]
    verified: Optional[bool]
    address: Optional[str]
    parking_number: Optional[str]

    img_link_1: Optional[str]
    img_link_2: Optional[str]
    img_link_3: Optional[str]

    verify_img: Optional[str]
    price_day: Optional[int]
    price_week: Optional[int]
    price_month: Optional[int]

    date_start: Optional[datetime.datetime]
    date_end: Optional[datetime.datetime]
    phone: Optional[int]
    comment: Optional[str]

    state: Optional[str]
    name: Optional[str]
