from django.test import LiveServerTestCase
from requests.auth import HTTPBasicAuth
from rest_framework.test import RequestsClient

from django.contrib.auth import get_user_model
from blog.models import Tag


class TagApiTestCase(LiveServerTestCase):
    def setUp(self):
        self.u1 = get_user_model().objects.create_user(
            email="johann@gmail.com",
            password="admin-oc"
        )

        self.tag_values = {"glenans", "voile", "hobiecat", "ffv"}
        for tag in self.tag_values:
            Tag.objects.create(value=tag)
        self.client = RequestsClient()

    def test_tag_list(self):
        response = self.client.get(self.live_server_url + "/api/v1/tags/")
        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 4)
        for tag_dict in data:
            tag = Tag.objects.get(pk=tag_dict["id"])
            self.assertEqual(tag_dict["value"], tag.value)

    def test_tag_create_basic_auth(self):
        self.client.auth = HTTPBasicAuth("johann@gmail.com", "admin-oc")

        response = self.client.post(self.live_server_url + "/api/v1/tags/", {"value": "marseillan"})
        data = response.json()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Tag.objects.count(), 5)
        tag = Tag.objects.get(pk=data["id"])
        self.assertEqual(tag.value, data["value"])

    def test_tag_create_token_auth(self):
        token_resp = self.client.post(self.live_server_url + "/api/v1/token-auth/", {"username": "johann@gmail.com", "password": "admin-oc"})
        self.client.headers["Authorization"] = "Token " + token_resp.json()["token"]

        response = self.client.post(self.live_server_url + "/api/v1/tags/", {"value": "marseillan"})
        data = response.json()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Tag.objects.count(), 5)
        tag = Tag.objects.get(pk=data["id"])
        self.assertEqual(tag.value, data["value"])