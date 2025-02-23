#Vance David G. Samia
from fastapi import FastAPI, Depends
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from typing import List, Optional
import os

# Initialize FastAPI app
app = FastAPI()

# MongoDB Connection
MONGO_URI = os.getenv("MONGO_URI", "your-mongodb-cloud-uri")
client = AsyncIOMotorClient(MONGO_URI)
db = client.eventlink

def get_db():
    return db
