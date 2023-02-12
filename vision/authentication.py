"""Computer Vision SDK for Python

This module is the Computer Vision SDK for Python.
The SDK allows clients to develop applications with little effort.
This script checks to see if authentication is allowed for communication with the Computer Vision API.

"""
import requests
from . import schemas as sh

class CognitiveServicesCredentials():
    """Confirm permission to connect to Computer Vision API
    """
    def __init__(self, key: str):
        self.endpoint: str = 'http://127.0.0.1:8000/authentication'
        self.key: str = key
    
    def authenticate(self) -> sh.CognitiveServicesCredentials:
        data: sh.Key = {
            'key': self.key
        }
        credentials = requests.post(url=self.endpoint, json=data).json()
        return credentials
