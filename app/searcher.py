import torch
import clip
from PIL import Image
import numpy as np
import faiss
import requests
from io import BytesIO

class ImageSearcher:
    def __init__(self, index_path="data/embeddings.index", metadata=None, device="cpu"):
        #can be changed to gpu later
        self.device = device
        #loading the CLIP model (ViT-B/32 variant) 
        self.model, self.preprocess = clip.load("ViT-B/32", device=device)
        # loading the FAISS index for search 
        self.index = faiss.read_index(index_path)
        self.metadata = metadata or []


    def search_text(self, query: str, top_k=1):

        """
        Search for images based on a text query using CLIP and FAISS.

        Args:
            query (str): The text query to search for.
            top_k (int): Number of top results to return.

        Returns:
            List: A list of metadata entries corresponding to the top matching images.
        """
        
        # Ensures PyTorch doesn't track gradients (saves memory and computation since we're only doing inference)
        
        with torch.no_grad():
            text = clip.tokenize([query]).to(self.device)
            # Encodes the text using CLIP’s text encoder, converts it to NumPy format on the CPU.
            embedding = self.model.encode_text(text).cpu().numpy()
        # Normalizes the embedding to unit length
        embedding /= np.linalg.norm(embedding)
        D, I = self.index.search(embedding, top_k)
        return [self.metadata[i] for i in I[0]]



    def search_image_url(self, url: str, top_k=1):
        """
        Search for similar images based on an image URL using CLIP and FAISS.

        Args:
            url (str): The URL of the image to use as the query.
            top_k (int): Number of top results to return.

        Returns:
            List: A list of metadata entries corresponding to the top matching images.
        """
        #downloads image from URL
        response = requests.get(url)
        image = Image.open(BytesIO(response.content)).convert("RGB")
        image = self.preprocess(image).unsqueeze(0).to(self.device)
        # preprocessing step for CLIP
        """
        Ensures PyTorch doesn't track gradients (saves memory and computation since we're only doing inference)
        """
        with torch.no_grad():
            embedding = self.model.encode_image(image).cpu().numpy()
        #Normalizes the image embedding.
        embedding /= np.linalg.norm(embedding)
        D, I = self.index.search(embedding, top_k)
        return [self.metadata[i] for i in I[0]]