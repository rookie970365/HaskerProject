from random import choices
from string import ascii_letters, digits

from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

TEST_USER = "".join(choices(ascii_letters, k=15))
TEST_PASSWORD = "".join(choices(ascii_letters + digits, k=10))


class DataSetup(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(username=TEST_USER, password=TEST_PASSWORD)
        self.password = TEST_PASSWORD
        self.user.save()

    def tearDown(self):
        self.user.delete()


class TestLogIn(DataSetup):
    def test_GET_unauthorized(self):
        client = Client()
        response = client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("account/login.html")

    def test_GET_authorized(self):
        client = Client()
        client.login(username=TEST_USER, password=TEST_PASSWORD)
        response = client.get(reverse("login"))

        self.assertEqual(response.status_code, 200)
        self.assertInHTML("<p>You have already logged in.</p>", str(response.content))
        self.assertInHTML("<h3>Log Out</h3>", str(response.content))

    def test_POST_authorized(self):
        client = Client()
        client.login(username=TEST_USER, password=TEST_PASSWORD)
        response = client.post(reverse("login"))

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("index"), response.url)

        response = client.post(reverse("login"), follow=True)
        self.assertRedirects(response, reverse("index"))
        self.assertInHTML("<p>You have already logged in.</p>", str(response.content))

    def test_POST_unauthorized(self):
        client = Client()
        response = client.post(
            reverse("login"),
            data={"username": TEST_USER, "password": TEST_PASSWORD},
            follow=True,
        )
        self.assertRedirects(response, reverse("index"))
        self.assertInHTML("<p>You have successfully logged in!</p>", str(response.content))


class TestLogOut(DataSetup):
    def test_POST_unauthorized(self):
        client = Client()
        response = client.post(reverse("logout"), data={}, follow=True)

        self.assertRedirects(response, reverse("index"))
        self.assertInHTML("<p>You are not authenticated!</p>", str(response.content))

    def test_POST_authorized(self):
        client = Client()
        client.login(username=TEST_USER, password=TEST_PASSWORD)
        response = client.post(reverse("logout"), data={}, follow=True)

        self.assertRedirects(response, reverse("index"))
        self.assertInHTML("<p>You have successfully logged out.</p>", str(response.content))


class TestSignUp(DataSetup):
    def test_GET_unauthorized(self):
        client = Client()
        response = client.get(reverse("signup"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("account/signup.html")

    def test_GET_authorized(self):
        client = Client()
        client.login(username=TEST_USER, password=TEST_PASSWORD)
        response = client.get(reverse("signup"), follow=True)

        self.assertRedirects(response, reverse("index"))
        self.assertInHTML("<p>You have already logged in.</p>", str(response.content))

    def test_POST_authorized(self):
        client = Client()
        client.login(username=TEST_USER, password=TEST_PASSWORD)
        response = client.post(reverse("signup"), follow=True)

        self.assertRedirects(response, reverse("index"))
        self.assertInHTML("<p>You have already logged in.</p>", str(response.content))

    def test_POST_registration(self):
        client = Client()
        response = client.post(
            reverse("signup"),
            data={
                "username": "new_user",
                "email": "new_user@mail.xxx",
                "password1": "new_password_123",
                "password2": "new_password_123",
            },
            follow=True,
        )

        self.assertRedirects(response, reverse("index"))
        self.assertInHTML("<p>Thank you for registration!</p>", str(response.content))
        self.assertTrue(get_user_model().objects.filter(username="new_user").exists())


class TestSettings(DataSetup):
    def test_GET_unauthorized(self):
        client = Client()
        response = client.get(reverse("detail"))
        self.assertRedirects(
            response, reverse("login") + "?next=" + reverse("detail")
        )

    def test_GET_authorized(self):
        client = Client()
        client.login(username=TEST_USER, password=TEST_PASSWORD)
        response = client.get(reverse("detail"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("account/detail.html")

    def test_POST_unauthorized(self):
        client = Client()
        response = client.post(
            reverse("detail"), data={"email": "some_new_email@mail.xxx"}
        )
        self.assertRedirects(response, reverse("login") + "?next=" + reverse("detail"))

    def test_POST_authorized(self):
        client = Client()
        client.login(username=TEST_USER, password=TEST_PASSWORD)
        response = client.post(
            reverse("detail"),
            data={"email": "some_new_email@mail.xxx"},
            follow=True,
        )
        self.assertRedirects(response, reverse("detail"))
        self.assertInHTML(
            "<p>Account details have been successfully updated!</p>",
            str(response.content),
        )
        self.user.refresh_from_db()

