from dotenv import load_dotenv
import os

load_dotenv()

api_key=os.getenv('GOOGLE_API_KEY')
print('Load api key',bool(api_key))

from dotenv import load_dotenv
load_dotenv()

from rag.embeddings import embeddings

vec = embeddings.embed_query("How do I reset my password?")
print(len(vec))