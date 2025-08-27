import faiss, json
from sentence_transformers import SentenceTransformer
import numpy as np
import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.0-flash")

def summarize_context(context, max_length=600):
 
    if len(context) > max_length:
        return context[:max_length] + "..."
    return context

def load_index_and_metadata(index_path, meta_path):
    index = faiss.read_index(index_path)
    with open(meta_path, "r", encoding="utf-8") as f:
        metadata = json.load(f)
    return index, metadata

def rag_search(query, index, metadata, num_results=5):
    
    query_embedding = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2").encode([query])
    
    distances, indices = index.search(np.array(query_embedding, dtype="float32"), num_results)
    
    relevant_docs = [metadata[i] for i in indices[0]]
    
    return relevant_docs

def generate_short_answer(query, relevant_docs):
    context = ""
    for doc in relevant_docs:
        context += f"Title: {doc['Series_Title']}, Description: {doc['Overview']}\n"
        

    prompt = (f"You are a friendly assistant who summarizes movies.\n"
        f"Respond based on the given plot.\n"
        f"Do NOT invent characters, event.\n"
        f"If someone asks you to recommend movies of a certain genre, provide them with what you know.\n"
        f"If the film is not in the database, respond that unfortunately you cannot say anything about this...\n"
        f"Start with a natural phrase like 'Sure!', 'Of course!', or 'Here's what I know:'.\n\n"
        f"Context: {summarize_context(context)}\nQuery: {query}")
    
    response = model.generate_content(prompt)
    return response.text