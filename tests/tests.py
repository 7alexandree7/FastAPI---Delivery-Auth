import requests

headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2IiwiZXhwIjoxNzcwOTMwMjc0fQ.mpgw3OAaPKhhi-DRCyNSjpuoqLc3AYNzh4i0uWDrw-8"
}

req = requests.get("http://127.0.0.1:8000/auth/refresh", headers=headers)
print(req)
print(req.json())