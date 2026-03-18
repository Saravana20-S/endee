
# rag/generator.py
import time
from google import genai
from config.settings import settings

class CodeMentor:
    def __init__(self):
     
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)
        
      
        self.model_candidates = [
            "gemini-2.5-flash", 
            "gemini-2.5-flash-lite",
            "gemini-1.5-flash-002"
        ]

    def generate_answer(self, question, context_chunks):
        context_text = "\n".join([f"Snippet {i+1}: {c}" for i, c in enumerate(context_chunks)])
        prompt = f"Context: {context_text}\n\nQuestion: {question}"
        
        for model_id in self.model_candidates:
            try:
                print(f"DEBUG: Trying 2026 Standard Model: {model_id}...")
                response = self.client.models.generate_content(
                    model=model_id, 
                    contents=prompt
                )
                if response and response.text:
                    return f"✅ ({model_id})\n{response.text}"
            except Exception as e:
                err = str(e)
                if "429" in err:
                    print(f"⚠️ {model_id} Quota Full (Limit 0). Trying next...")
                    continue
                if "404" in err:
                    print(f"❌ {model_id} not available in your region/tier.")
                    continue
                print(f"❌ Unexpected Error with {model_id}: {err[:100]}")
        
        return "❌ All 2026 Free Models failed. Check AI Studio for 'Gemini 2.5' availability."

generator = CodeMentor()