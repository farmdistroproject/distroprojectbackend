import httpx 
import os, hmac, hashlib, json
from fastapi import APIRouter, Depends, Request
from user.helpers import get_current_user
from sqlalchemy.orm import Session
from user.models import User
from config.database import get_db
from payment.models import Transaction

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
        output = client.post(URL, headers=headers, data=body)
        return output.json()
        

@router.post("/webhook-verify")
async def check_event_status(request:Request, db:Session=Depends(get_db)):
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
        current_payer = db.query(User).filter(User.email == json_output['data']['customer']['email']).first()
        print(current_payer.email)
        new_balance = json_output['data']['amount'] / 100
        log_transaction = Transaction(user=current_payer.id,
                                              balance=current_payer.wallet_balance, 
                                              amount_added=new_balance, 
                                              status= json_output['data']['status'],
                                                channel=json_output['data']['channel'],
                                                 gateway_response=json_output['data']['gateway_response'],
                                                  created_at=json_output['data']['created_at'],
                                                   paid_at=json_output['data']['paid_at'] )
        current_payer.wallet_balance += new_balance
        db.add(log_transaction)
        db.commit()
        print({"email":current_payer.email,"wallet_balance":current_payer.wallet_balance})       
    else:
        print(json_output['event'],current_payer.email)
        