"""
This file sets up a FastAPI web service for indexing and searching images using CLIP and FAISS. It defines three endpoints:

/index: Takes a list of image URLs and indexes them using the ImageIndexer class, saving the embeddings and metadata.

/search/text: Takes a text query and returns the most relevant images based on similarity, using the ImageSearcher.

/search/image: Takes an image URL and returns similar images by searching through pre-indexed embeddings using ImageSearcher.

"""


from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import List
from app.indexer import ImageIndexer
from app.searcher import ImageSearcher
import os
import json

app = FastAPI()
indexer = ImageIndexer()

class IndexRequest(BaseModel):
    urls: List[str]

@app.post("/index")
def index_images(req: IndexRequest):
    """
    Index a list of image URLs by adding them to the image search index.

    Args:
        req (IndexRequest): A request object containing a list of image URLs to index.

    Returns:
        dict: A JSON response indicating success and the number of images indexed.
    """
    for url in req.urls:
        indexer.add_image(url)
    indexer.save_index()
    with open("data/metadata.json", "w") as f:
        json.dump(indexer.metadata, f)
    return {"status": "success", "indexed": len(req.urls)}

@app.get("/search/text")
def search_text(q: str):
    """
    Search for images using a text query.

    Args:
        q (str): The text query to search for.

    Returns:
        List: A list of metadata entries corresponding to the most relevant images.
    """
    with open("data/metadata.json") as f:
        metadata = json.load(f)
    searcher = ImageSearcher(metadata=metadata)
    results = searcher.search_text(q)
    return results

@app.get("/search/image")

def search_image(image_url: str = Query(...)):
    """
    Search for images similar to the one at the provided image URL.

    Args:
        image_url (str): The URL of the query image.

    Returns:
        List: A list of metadata entries corresponding to the most similar images.
    """
    with open("data/metadata.json") as f:
        metadata = json.load(f)
    searcher = ImageSearcher(metadata=metadata)
    results = searcher.search_image_url(image_url)
    return results
