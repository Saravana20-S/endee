

# vectordb/endee_client.py
import requests
import time
import json
from config.settings import settings

class EndeeClient:
    def __init__(self):
        # Ensure base_url points to the root (e.g., http://localhost:8000/api/v1)
        self.base_url = settings.ENDEE_URL.rstrip('/')

    def _safe_response(self, response):
        try:
            return response.json()
        except Exception:
            return {"status_code": response.status_code, "raw_body": response.text}

    def create_index(self, index_name, dimension=384):
        # Path: /index/create
        url = f"{self.base_url}/index/create"
        payload = {
            "index_name": index_name,
            "dim": dimension,
            "space_type": "cosine"
        }
        response = requests.post(url, json=payload)
        return self._safe_response(response)

    def insert_vectors(self, index_name, vectors, metadata_list):
        # Path: /index/{name}/vector/insert
        url = f"{self.base_url}/index/{index_name}/vector/insert"
        payload = []
        for i, (vec, meta) in enumerate(zip(vectors, metadata_list)):
            # Your clean_meta logic is perfect—keeps DB happy
            clean_meta = {str(k): str(v) for k, v in meta.items()}
            
            payload.append({
                "id": str(int(time.time()) + i),
                "vector": [float(x) for x in vec],
                "meta": clean_meta,
                "filter": {"source": "github"} 
            })
            
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        return self._safe_response(response)

    def search_vectors(self, index_name, query_vector, k=3):
        # Path updated to match tutorial: /index/{name}/vector/search
        url = f"{self.base_url}/index/{index_name}/vector/search"
        payload = {
            "vector": [float(x) for x in query_vector],
            "top_k": k
        }
        response = requests.post(url, json=payload)
        return self._safe_response(response)

    def delete_index(self, index_name):
        # Path: /index/{name}/delete
        url = f"{self.base_url}/index/{index_name}/delete"
        try:
            # Note: Many Endee versions use POST for delete endpoints, 
            # but we'll try DELETE first as per standard REST.
            response = requests.delete(url)
            return response.status_code == 200
        except Exception as e:
            print(f"Delete error: {e}")
            return False

endee_client = EndeeClient()





# # vectordb/endee_client.py
# import requests
# import time
# import json
# from config.settings import settings

# class EndeeClient:
#     def __init__(self):
#         self.base_url = settings.ENDEE_URL.rstrip('/')

#     def _safe_response(self, response):
#         try:
#             return response.json()
#         except Exception:
#             return {"status_code": response.status_code, "raw_body": response.text}

#     def create_index(self, index_name, dimension=384):
#         url = f"{self.base_url}/index/create"
#         payload = {
#             "index_name": str(index_name),
#             "dim": 384,
#             "space_type": "cosine"
#         }
#         response = requests.post(url, json=payload)
#         return self._safe_response(response)

#     def insert_vectors(self, index_name, vectors, metadata_list):
#         """
#         FIX: The 'value is not string' error usually happens in the 'ids' 
#         or 'metas' fields. We force-stringify everything here.
#         """
#         url = f"{self.base_url}/index/{index_name}/vector/insert"
        
#         # 1. Prepare strictly stringified IDs
#         # We use a unique timestamp + index to avoid collisions
#         base_ts = int(time.time())
#         clean_ids = [str(base_ts + i) for i in range(len(vectors))]
        
#         # 2. Prepare strictly stringified Metadata
#         clean_metas = []
#         for meta in metadata_list:
#             # Force every key and every value to be a STRING
#             sanitized = {str(k): str(v) for k, v in meta.items()}
#             clean_metas.append(sanitized)

#         # 3. Ensure vectors are standard Python floats (not numpy types)
#         clean_vectors = [[float(val) for val in vec] for vec in vectors]

#         # 4. Construct Payload
#         payload = {
#             "vectors": clean_vectors,
#             "metas": clean_metas,
#             "ids": clean_ids
#         }
            
#         try:
#             # Use json.dumps to ensure clean serialization
#             response = requests.post(
#                 url, 
#                 data=json.dumps(payload), 
#                 headers={'Content-Type': 'application/json'},
#                 timeout=30
#             )
#             return self._safe_response(response)
#         except Exception as e:
#             print(f"❌ Insert Error: {e}")
#             return None

#     def search_vectors(self, index_name, query_vector, k=3):
#         url = f"{self.base_url}/index/{index_name}/vector/search"
#         payload = {
#             "vector": [float(x) for x in query_vector],
#             "top_k": int(k)
#         }
#         response = requests.post(url, json=payload)
#         return self._safe_response(response)

#     def delete_index(self, index_name):
#         url = f"{self.base_url}/index/{index_name}/delete"
#         try:
#             # Endee often prefers POST for the delete action
#             response = requests.post(url)
#             if response.status_code != 200:
#                 response = requests.delete(url)
#             return response.status_code == 200
#         except Exception:
#             return False

# endee_client = EndeeClient()