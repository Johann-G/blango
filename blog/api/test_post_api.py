from datetime import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from pytz import UTC
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from blog.models import Post


class PostApiTestCase(TestCase):
    def setUp(self):
        self.u1 = get_user_model().objects.create_user(
            email="johann@gmail.com",
            password="admin-oc"
        )
        self.u2 = get_user_model().objects.create_user(
            email="camille@gmail.com",
            password="admin-oc"
        )

        posts = [
            Post.objects.create(
                author=self.u1,
                published_at=timezone.now(),
                title="Titre du premier poste",
                slug="titre-du-premier-poste",
                summary="Résumé du premier poste",
                content="Contenu du premier poste",
            ),
            Post.objects.create(
                author=self.u2,
                published_at=timezone.now(),
                title="Titre du deuxième poste",
                slug="titre-du-deuxieme-poste",
                summary="Résumé du deuxième poste",
                content="Contenu du deuxième poste",
            )
        ]
        self.post_by_id = {post.id: post for post in posts}

        self.client = APIClient()
        token = Token.objects.create(user=self.u1)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)

    def test_post_list(self):
        response = self.client.get("/api/v1/posts/")
        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 2)
        for post_dict in data:
            post = self.post_by_id[post_dict["id"]]

            self.assertEqual(post_dict["title"], post.title)
            self.assertEqual(post_dict["slug"], post.slug)
            self.assertEqual(post_dict["summary"], post.summary)
            self.assertEqual(post_dict["content"], post.content)
            self.assertTrue(post_dict["author"].endswith(f"/api/v1/users/{post.author.email}"))
            self.assertEqual(datetime.strptime(post_dict["published_at"], "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=UTC), post.published_at)

    def test_unauthenticated_post_create(self):
        self.client.credentials()

        body = {
            "title": "Test Post",
            "slug": "test-post-3",
            "summary": "Test Post Summary",
            "content": "Test Content",
            "author": "http://testserver/api/v1/users/johann@gmail.com",
            "published_at": "2021-01-10T09:00:00Z",
        }
        response = self.client.post("/api/v1/posts/", body)
        data = response.json()

        self.assertEqual(response.status_code, 401)
        self.assertEqual(Post.objects.count(), 2)

    def test_post_create(self):
        body = {
            "title": "Test Post",
            "slug": "test-post-3",
            "summary": "Test Post Summary",
            "content": "Test Content",
            "author": "http://testserver/api/v1/users/johann@gmail.com",
            "published_at": "2021-01-10T09:00:00Z",
        }
        response = self.client.post("/api/v1/posts/", body)
        data = response.json()

        post = Post.objects.get(pk=data["id"])

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Post.objects.count(), 3)
        self.assertEqual(body["title"], post.title)
        self.assertEqual(body["summary"], post.summary)
        self.assertEqual(body["content"], post.content)
        self.assertEqual(body["slug"], post.slug)
        self.assertTrue(body["author"].endswith(f"/api/v1/users/{post.author.email}"))
        self.assertEqual(datetime(2021, 1, 10, 9, 0, 0, tzinfo=UTC), post.published_at)


