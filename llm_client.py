import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

class LLMClient:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.model = None
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-flash-latest')

    def generate_response(self, messages, temperature=0.7):
        if not self.model:
            return "Error: Gemini API Key not found. Please set GEMINI_API_KEY environment variable."
        
        try:
            # Separate system prompt if present
            system_instruction = ""
            gemini_history = []
            
            for msg in messages:
                role = msg["role"]
                content = msg["content"]
                if role == "system":
                    system_instruction += content + "\n"
                elif role == "user":
                    gemini_history.append({"role": "user", "parts": [content]})
                elif role == "assistant":
                    gemini_history.append({"role": "model", "parts": [content]})
            
            # Use a model with system instruction if needed
            if system_instruction:
                # Re-instantiate model with system instruction
                # We do this per request to be safe with state, though less efficient
                current_model = genai.GenerativeModel('gemini-flash-latest', system_instruction=system_instruction)
            else:
                current_model = self.model

            # Prepare chat history and last message
            chat_history = []
            last_message = None

            if gemini_history:
                last_msg_obj = gemini_history[-1]
                if last_msg_obj['role'] == 'user':
                    last_message = last_msg_obj['parts'][0]
                    chat_history = gemini_history[:-1]
                else:
                     # If the last message isn't a user message, we can't trigger a generation easily 
                     # in a chat context without a user prompt.
                     # But for this agent, it should always end with user input.
                     return "Error: Last message in history must be from user."
            else:
                return "Error: No message history to generate from."

            chat = current_model.start_chat(history=chat_history)
            response = chat.send_message(last_message, generation_config=genai.types.GenerationConfig(temperature=temperature))
            
            return response.text
        except Exception as e:
            print(f"DEBUG: Gemini Error: {e}")
            return f"Error communicating with Gemini: {str(e)}"
