import json
import os
from sentence_transformers import SentenceTransformer
import numpy as np

# Load model lazily at first use
model = None

# Store data in memory
menu_items = []
menu_embeddings = []


def get_model():
    global model
    if model is None:
        model = SentenceTransformer("all-MiniLM-L6-v2")
    return model

# Correct path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "menu.json")


# 🔹 Load and embed menu
def create_embeddings():
    global menu_items, menu_embeddings

    print("📂 Loading menu from:", DATA_PATH)

    if not os.path.exists(DATA_PATH):
        print("❌ menu.json not found!")
        return

    with open(DATA_PATH, "r") as f:
        data = json.load(f)

    if not data:
        print("❌ menu.json is empty!")
        return

    menu_items = data

    texts = [
        f"{item['name']} {item['category']} {item['meal_type']} {item['type']} {item['spicy']} {item['oil']}"
        for item in data
    ]

    print("⚙️ Creating embeddings...")
    menu_embeddings = get_model().encode(texts)

    print("✅ Embeddings ready!")


# 🔹 Cosine similarity
def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


# 🔹 Query menu
def query_menu(query: str):
    global menu_items, menu_embeddings

    # Return all items
    if not query.strip():
        print("🔍 Returning all items")
        return menu_items

    if len(menu_embeddings) == 0:
        print("❌ Embeddings not created!")
        return []

    query_vec = get_model().encode(query)

    scores = [
        cosine_similarity(query_vec, emb)
        for emb in menu_embeddings
    ]

    # Get top 5
    top_indices = np.argsort(scores)[-5:][::-1]

    results = [menu_items[i] for i in top_indices if scores[i] > 0.3]

    return results