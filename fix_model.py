import shutil
import os
from langchain_community.embeddings import HuggingFaceEmbeddings

# 1. Define the path to the broken cache
user_home = os.path.expanduser("~")
cache_path = os.path.join(user_home, ".cache", "huggingface", "hub", "models--sentence-transformers--all-MiniLM-L6-v2")

# 2. Delete it if it exists (Cleaning up the corruption)
if os.path.exists(cache_path):
    print(f"🗑️  Found corrupted model. Deleting: {cache_path}")
    try:
        shutil.rmtree(cache_path)
        print("✅ Cache cleared.")
    except Exception as e:
        print(f"❌ Error deleting cache: {e}")
        print("👉 Please try deleting that folder manually.")
else:
    print("✅ No corrupted cache found.")

# 3. Download it fresh
print("⬇️  Downloading the model fresh... (This usually takes 30-60 seconds)")
try:
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    print("🎉 Success! The model is fixed and ready.")
except Exception as e:
    print(f"❌ Download failed: {e}")