from pydantic import BaseModel


class PlansBase(BaseModel):
    name : str
    description :str
    duration : int
    price : int
    create_at : str



class PlansListView(BaseModel):
    id : str
    name : str
    description :str
    duration : int
    price : int
    create_at : str