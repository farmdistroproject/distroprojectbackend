import httpx 
import os, hmac, hashlib
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
        

@router.get("/verify-payment") 
async def Verify_Payment(reference:str, request:Request, user:dict= Depends(get_current_user), db:Session=Depends(get_db)):
    url=f"https://api.paystack.co/transaction/verify/{reference}"
    secret_key = os.getenv("PAYSTACK_SECRET_KEY")
    headers = {'authorization': f"Bearer {secret_key}"}
    with httpx.Client() as client:
        r=client.get(url, headers=headers)
        output=r.json()
        if output['status'] == True:
            current_payer = db.query(models.User).filter(models.User.email == output['data']['customer']['email']).first()
            current_payer.wallet_balance = output['data']['amount']
            db.commit()
            db.close()
            return current_payer



# Testing Webhook Verification to update user wallet_balance

@router.post("/webhook-verify")
async def check_event_status(request:Request, response:Response, db:Session=Depends(get_db)):
    key = os.getenv("WEBHOOK_SECRET_KEY")
    byte_key = bytearray(key, 'utf-8')
    hashed_key = hmac.new(byte_key, msg=None, digestmod=hashlib.sha512).hexdigest()
    requested_header = request.headers['x-paystack-signature']
    if hashed_key == requested_header:
        output = request.json()
        if output['event'] == "charge.success":
            current_payer = db.query(models.User).filter(models.User.email == output['data']['customer']['email']).first()
            print(current_payer)
            current_payer.wallet_balance = output['data']['amount']
            db.commit()
            db.close()
            return {"email":current_payer.email,"wallet_balance":current_payer.wallet_balance}