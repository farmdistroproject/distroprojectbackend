from typing import Union
from fastapi import FastAPI
from user import router as user_router


app = FastAPI()
app.include_router(user_router.router)


#using this to test the oauth

from fastapi import  Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="templates")



# app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("signin.html", {"request": request})
