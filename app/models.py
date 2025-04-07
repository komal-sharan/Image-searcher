"""
This file defines a dataclass called ImageMetadata, which is used to store information about each image. The class contains three attributes:

url: The URL of the image.

filepath: The local path where the image is stored.

embedding: A list of floating-point numbers representing the image's feature vector (embedding).

"""

from dataclasses import dataclass
from typing import List

@dataclass
class ImageMetadata:
    url: str
    filepath: str
    embedding: List[float]