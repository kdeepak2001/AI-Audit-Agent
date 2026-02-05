import google.generativeai as genai
import os

api_key = os.environ.get("GOOGLE_API_KEY")

if not api_key:
    print("❌ Error: GOOGLE_API_KEY is not set.")
else:
    print(f"✅ Key Found: {api_key[:5]}...{api_key[-3:]}")
    print("\n🔎 Scanning Google for YOUR available models...")
    
    genai.configure(api_key=api_key)
    
    found_any = False
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"   👉 {m.name}")
            found_any = True
            
    if not found_any:
        print("❌ No Chat models found. Your key might have restricted permissions.")