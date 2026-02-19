import os
from dotenv import load_dotenv

print(f"CWD: {os.getcwd()}")
env_path = os.path.join(os.getcwd(), ".env")
print(f".env exists: {os.path.exists(env_path)}")

if os.path.exists(env_path):
    with open(env_path, "r") as f:
        content = f.read()
        print(f".env content length: {len(content)}")
        print(f"First line: {content.splitlines()[0] if content else 'EMPTY'}")

print("Loading dotenv...")
load_dotenv(verbose=True)
api_key = os.getenv("GEMINI_API_KEY")
print(f"GEMINI_API_KEY from env: {api_key[:5] if api_key else 'None'}")
