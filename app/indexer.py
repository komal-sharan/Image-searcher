"""
This file defines an ImageIndexer class that uses the CLIP model and FAISS to index images. It includes methods to add images to the index by downloading them, preprocessing, and encoding them into embeddings, then saving the index to disk. The class stores image metadata, such as URLs and file paths, alongside the embeddings in a FAISS index for efficient similarity search.
"""

import torch
import clip
from PIL import Image
from app.utils import download_image
import faiss
import os
import numpy as np

class ImageIndexer:
    def __init__(self, device="cpu"):
        self.device = device
        self.model, self.preprocess = clip.load("ViT-B/32", device=device)
        self.index = faiss.IndexFlatIP(512)
        self.metadata = []

    def add_image(self, url: str):
        """
            Downloads an image from a URL, preprocesses it, generates an embedding, 
            normalizes the embedding, and adds it to the FAISS index along with metadata.

            Args:
                url (str): The URL of the image to be indexed.

            Returns:
                None: This function does not return any value. It modifies the FAISS index and metadata in place.
        """
        filepath = download_image(url)
        image = self.preprocess(Image.open(filepath)).unsqueeze(0).to(self.device)
        with torch.no_grad():
            embedding = self.model.encode_image(image).cpu().numpy()
        norm = np.linalg.norm(embedding)
        embedding /= norm
        self.index.add(embedding)
        self.metadata.append({"url": url, "filepath": filepath})

    def save_index(self, path="data/embeddings.index"):
        """
        Saves the FAISS index to a specified file path.

         Args:
            path (str): The file path where the FAISS index will be saved. Default is "data/embeddings.index".

        Returns:
            None: This function does not return any value. It saves the FAISS index to disk.
        """
        faiss.write_index(self.index, path)