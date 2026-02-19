import sys
import os
import traceback

print("Starting verification...", flush=True)

try:
    import google.generativeai as genai
    print("Import successful.", flush=True)
except ImportError as e:
    print(f"Import failed: {e}", flush=True)
    sys.exit(1)

from llm_client import LLMClient

def test_generation():
    print("Initializing Client...", flush=True)
    try:
        client = LLMClient()
        if not client.api_key:
            print("Error: API Key not found in env.", flush=True)
            return
        
        print(f"API Key present: {client.api_key[:5]}...", flush=True)
        
        messages = [{"role": "user", "content": "Say hello"}]
        print("Sending request...", flush=True)
        response = client.generate_response(messages)
        print(f"Response: {response}", flush=True)
        
    except Exception:
        traceback.print_exc()

if __name__ == "__main__":
    test_generation()
