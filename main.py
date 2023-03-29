from typing import Union
from fastapi import FastAPI
from user import router as user_router
from payment import router as payment_router
from product import router  as plans_router

app = FastAPI(description="Ntoju backend",title="Ntoju dev")
app.include_router(user_router.router)
app.include_router(payment_router.router)
app.include_router(plans_router.router)




@app.get("/")
async def root():
    return "you dey homepage"
