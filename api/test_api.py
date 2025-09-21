# test_api.py
import requests

url = "http://localhost:8000/api/storytelling/generate"
data = {
    "description": "Blue pot with peacock and lotus flowers, traditional Jaipur techniques"
}

response = requests.post(url, data=data)
print("Status Code:", response.status_code)
print("Response:", response.json())