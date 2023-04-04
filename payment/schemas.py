from pydantic import BaseModel
from datetime import datetime

class Transaction(BaseModel):
    id:int
    user_email:str
    balance: int
    amount_added: int
    reference: str
    status: str
    channel: str
    gateway_response: str
    created_at: datetime
    paid_at: datetime

    class Config:
        orm_mode = True