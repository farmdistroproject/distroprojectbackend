from typing import Union
from fastapi import FastAPI


app = FastAPI()

@app.get("/")
async def root():
    return{"introduction": "ntoju backend server"}