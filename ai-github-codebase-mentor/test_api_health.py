# test_api_health.py
from rag.generator import generator

print("--- API HEALTH CHECK ---")
generator.check_available_models()

print("\n--- TEST QUESTION ---")
print(generator.generate_answer("Hello", ["Test context"]))