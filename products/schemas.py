from pydantic import BaseModel
from uuid import UUID

class ProductBase(BaseModel):
    name : str
    description :str
    price : int




class ProductListView(BaseModel):
    id : UUID
    name : str
    description :str
    price : int
    create_at : str

    class Config():
        orm_mode = True


class ProductUpdateSchema(BaseModel):
    name : str
    description :str
    price : int