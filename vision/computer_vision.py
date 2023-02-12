"""Computer Vision SDK for Python

This module is the Computer Vision SDK for Python.
The SDK allows clients to develop applications with little effort.
By sending an image to the Computer Vision API, the client can receive the result of whether or not the person in the image is wearing a mask.

"""

import requests
import json
from . import schemas as sh

class ComputerVisionClient():
    """Connect with Computer Vision API
    """
    def __init__(self, endpoint: str, credentials: sh.CognitiveServicesCredentials):
        # Set up endpoints if credentials passes
        if credentials['authentication']:
            self.endpoint = endpoint
        else:
            print('AUTHENTICATION ERROR: Your key does not allow authentication. Please check your key again.')

    def detect_mask(self, image: list) -> json:
        """Person detection and determination of whether or not a person is wearing a mask

        Args:
            image (list): Input image.

        Returns:
            json: Response from API server.
        """
        detect_endopoint: str = self.endpoint + '/detect_mask'
        data: sh.Data = {
            'image': image
        }
        res = requests.post(url=detect_endopoint, json=data)
        return res