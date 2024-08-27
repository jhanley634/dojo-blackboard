"""
Main web server for the Blackboard application.

usage:  $ fastapi dev src/bboard/main.py
"""

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello Dojo!"}
