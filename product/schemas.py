from pydantic import BaseModel
from uuid import UUID

class PlansBase(BaseModel):
    name : str
    description :str
    duration : int
    price : int
    create_at : str



class PlansListView(BaseModel):
    id : UUID
    name : str
    description :str
    duration : int
    price : int
    create_at : str

    class Config():
        orm_mode = True


class PlanUpdateSchema(BaseModel):
    name : str
    description :str
    duration : int
    price : int