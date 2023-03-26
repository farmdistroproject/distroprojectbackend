import httpx 
import os, hmac, hashlib, json
from fastapi import APIRouter, Depends, Request, Response
from user.helpers import get_current_user
from sqlalchemy.orm import Session
from user import models
from config.database import get_db
from logging import Logger

router = APIRouter()

@router.post("/fund-wallet", response_model=None)
async def Initialize_Payment(amount:int, user:dict= Depends(get_current_user)):
    """Use in the Checkout Page"""
    URL="https://api.paystack.co/transaction/initialize"
    secret_key = os.getenv("PAYSTACK_SECRET_KEY")
    headers = {'authorization': f"Bearer {secret_key}"}
    converted_amount = amount*100
    body = {'email': user.email, 'amount':converted_amount}
    with httpx.Client() as client:
        r = client.post(URL, headers=headers, data=body)
        return r.json()
        

@router.post("/webhook-verify")
async def check_event_status(request:Request, response:Response, db:Session=Depends(get_db)):
    """Webhook Verification to update user wallet_balance"""
    key = os.getenv("WEBHOOK_SECRET_KEY")
    output = await request.body()
    byte_key = bytearray(key, 'utf-8')
    hashed_key = hmac.new(byte_key, msg=output, digestmod=hashlib.sha512).hexdigest()
    requested_header = request.headers.get('x-paystack-signature')
   
    if hashed_key != requested_header:
        print("Not Valid?")
    json_output=json.loads(output)
    if json_output['event'] == "charge.success":
        current_payer = db.query(models.User).filter(models.User.email == json_output['data']['customer']['email']).first()
        print(current_payer.email)
        current_payer.wallet_balance = json_output['data']['amount'] / 100
        db.commit()
        print({"email":current_payer.email,"wallet_balance":current_payer.wallet_balance})       

        