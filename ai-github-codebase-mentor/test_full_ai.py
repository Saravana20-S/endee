# test_full_ai.py
from rag.generator import generator
import time

# Mock context from our earlier successful database search
mock_context = ["def calculate_area(radius): return 3.14 * (radius ** 2)"]
question = "Explain how the area is calculated in this code."

print("--- Starting Final AI Test ---")
answer = generator.generate_answer(question, mock_context)
print("\n" + "="*30)
print(f"RESULT:\n{answer}")
print("="*30)