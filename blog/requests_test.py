import requests

EMAIL_ADDRESS = "nicolas@gmail.com"
PASSWORD = "admin-oc"
BASE_URL = "http://127.0.0.1:8000/"

anon_post_resp = requests.get(BASE_URL + "api/v1/posts/")
anon_post_resp.raise_for_status()
anon_post_count = anon_post_resp.json()["count"]
print(f"anon_post_count: {anon_post_count}")

auth_resp = requests.post(BASE_URL + "api/v1/token-auth/", json={"username": EMAIL_ADDRESS, "password": PASSWORD})
auth_resp.raise_for_status()
token = auth_resp.json()["token"]

authed_post_resp = requests.get(BASE_URL + "api/v1/posts/", headers={"Authorization": f"Token {token}"})
authed_post_resp.raise_for_status()
authed_post_count = authed_post_resp.json()["count"]
print(f"authed_post_count: {authed_post_count}")