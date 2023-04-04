from typing import Union
from fastapi import FastAPI
from user import router as user_router
from payment import router as payment_router
from plan import router  as plans_router
from products import router  as products_router
from cart import router as cart_router

app = FastAPI(description="Ntoju backend",title="Ntoju dev")
app.include_router(user_router.router)
app.include_router(payment_router.router)
app.include_router(plans_router.router)
app.include_router(cart_router.router)
app.include_router(products_router.router)




@app.get("/")
async def root():
    return "you dey homepage"
