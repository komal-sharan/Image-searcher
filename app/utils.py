import os
import requests
from PIL import Image
from io import BytesIO

def download_image(url: str, save_dir: str = "data/images") -> str:
    """
    Downloads an image from a URL and saves it to the specified directory.

    Args:
        url (str): The URL of the image to be downloaded.
        save_dir (str, optional): The directory where the image will be saved. Default is "data/images".

    Returns:
        str: The file path where the image was saved.
    """
    os.makedirs(save_dir, exist_ok=True)
    response = requests.get(url)
    response.raise_for_status()
    img = Image.open(BytesIO(response.content)).convert("RGB")
    filename = os.path.join(save_dir, os.path.basename(url.split("?")[0]))
    img.save(filename)
    return filename