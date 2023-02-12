"""Computer Vision SDK for Python

This module is the Computer Vision SDK for Python.
The SDK allows clients to develop applications with little effort.
This module declares the type of a variable based on a type hint.

"""
from pydantic import BaseModel

class Key(BaseModel):
    key: str

class CognitiveServicesCredentials(BaseModel):
    authentication: bool

class Data(BaseModel):
    image: list