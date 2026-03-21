

# vectordb/endee_client.py
import requests
import time
import json
import numpy as np
from config.settings import settings

class EndeeClient:
    def __init__(self):
        # Ensure base_url is clean (e.g., http://localhost:8080/api/v1)
        self.base_url = settings.ENDEE_URL.rstrip('/')

    def _safe_response(self, response):
        """Helper to handle JSON decoding and provide clear error logs."""
        try:
            return response.json()
        except Exception:
            return {
                "status_code": response.status_code, 
                "error": "Non-JSON response received",
                "raw_body": response.text[:500] # Cap for readability
            }

    def create_index(self, index_name, dimension=384):
        """Matches: POST /api/v1/index/create"""
        url = f"{self.base_url}/index/create"
        payload = {
            "index_name": index_name,
            "dim": dimension,
            "space_type": "cosine"
        }
        response = requests.post(url, json=payload)
        return self._safe_response(response)

    # def insert_vectors(self, index_name, vectors, metadata_list):
    #     """Matches: POST /api/v1/index/{index_name}/vector/insert"""
    #     url = f"{self.base_url}/index/{index_name}/vector/insert"
        
    #     payload = []
    #     for i, (vec, meta) in enumerate(zip(vectors, metadata_list)):
    #         # Force all metadata values to string to prevent "Value is not string" 500 errors
    #         clean_meta = {str(k): str(v) for k, v in meta.items()}
            
    #         payload.append({
    #             "id": f"vec_{int(time.time())}_{i}", # Professional ID format
    #             "vector": [float(x) for x in vec],
    #             "meta": clean_meta,
    #             "filter": {
    #                 "source": "github_mentor",
    #                 "timestamp": str(int(time.time()))
    #             }
    #         })
            
    #     headers = {'Content-Type': 'application/json'}
    #     # Using data=json.dumps to ensure strict formatting
    #     response = requests.post(url, data=json.dumps(payload), headers=headers)
    #     return self._safe_response(response)

  

    def insert_vectors(self, index_name, vectors, metadatas):
        sanitized_metas = [{str(k): str(v) for k, v in m.items()} for m in metadatas]
        
        payload = {
            "vectors": [list(v) for v in vectors],
            "metas": sanitized_metas
        }
        
        endpoint = f"{self.base_url}/index/{index_name}/vector/insert"

        try:
            response = requests.post(endpoint, json=payload)
            if response.status_code == 200:
                return True
            else:
                # This will print the "Failed to begin transaction" error to your Python console
                print(f"DEBUG: Status {response.status_code}, Body: {response.text}")
                return False
        except Exception as e:
            print(f"DEBUG: Request failed: {e}")
            return False

    def search_vectors(self, query_vector, index_name, k=5):
        """Matches: POST /api/v1/index/{index_name}/search"""
        url = f"{self.base_url}/index/{index_name}/search"
        payload = {
            "vector": [float(x) for x in query_vector],
            "k": k,
            "include_vectors": True # Useful for debugging in the UI
        }
        response = requests.post(url, json=payload)
        return self._safe_response(response)

    def get_index_stats(self, index_name):
        """Matches: GET /api/v1/index/{index_name}/stats - Essential for UI feedback"""
        url = f"{self.base_url}/index/{index_name}/stats"
        try:
            response = requests.get(url)
            return self._safe_response(response)
        except Exception as e:
            return {"error": str(e)}

    def delete_index(self, index_name):
        """Matches: POST /api/v1/index/delete"""
        url = f"{self.base_url}/index/delete"
        payload = {"index_name": index_name}
        try:
            # Endee Tutorial uses POST for deletion requests
            response = requests.post(url, json=payload)
            return response.status_code == 200 or response.status_code == 204
        except Exception as e:
            print(f"Delete error: {e}")
            return False

endee_client = EndeeClient()