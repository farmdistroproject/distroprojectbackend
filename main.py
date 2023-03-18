from typing import Union
from fastapi import FastAPI
from user import router as user_router


app = FastAPI(description="Ntoju backend",title="Ntoju dev")
app.include_router(user_router.router)





@app.get("/")
async def root():
    return "you dey homepage"
