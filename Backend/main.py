# this file will contain all the backend logic and routes of fastapi
from fastapi import FastAPI
from fastapi.exceptions import HTTPException


app = FastAPI()


@app.get("/")
async def welcome():
    return{
        "status":200,
        "message":"App is up."
    }



