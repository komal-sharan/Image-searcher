import streamlit as st
import requests

API_URL = "http://localhost:8000"

st.title("🖼️ Image Search Engine")

st.sidebar.header("Index New Images")
image_urls = st.sidebar.text_area("Enter image URLs (one per line):")
if st.sidebar.button("Index Images"):
    urls = image_urls.strip().split("\n")
    res = requests.post(f"{API_URL}/index", json={"urls": urls})
    st.sidebar.success(f"Indexed {res.json().get('indexed', 0)} images")

st.header("Search by Text")
text_query = st.text_input("Enter a description (e.g. 'a dog on the beach'):")
if st.button("Search Text"):
    res = requests.get(f"{API_URL}/search/text", params={"q": text_query})
    results = res.json()
    for r in results:
        st.image(r['url'], caption=r['url'], width=200)

st.header("Search by Image URL")
img_url = st.text_input("Enter image URL to search by similarity:")
if st.button("Search Image"):
    res = requests.get(f"{API_URL}/search/image", params={"image_url": img_url})
    results = res.json()
    for r in results:
        st.image(r['url'], caption=r['url'], width=200)