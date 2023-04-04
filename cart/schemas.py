from pydantic import BaseModel,EmailStr
from datetime import datetime,date,time
from typing import Union,Optional



class CartItem(BaseModel):
    product_id: str
    quantity: int

