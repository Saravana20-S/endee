# check_db.py
import requests
from config.settings import settings

def test_connection():
    try:
        # Endee usually has a /health or /index/list endpoint
        response = requests.get(f"{settings.ENDEE_URL}/index/list")
        if response.status_code == 200:
            print("✅ Success! Python is connected to Endee.")
            print("Current Indexes:", response.json())
        else:
            print(f"❌ Connected, but got error: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"❌ Failed to connect: {e}")

if __name__ == "__main__":
    test_connection()