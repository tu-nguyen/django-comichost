from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from .models import Comic, Review


class ComicTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="reviewuser",
            email="reviewuser@email.com",
            password="testpass123",
        )

        cls.special_permission = Permission.objects.get(
            codename="special_status"
        )

        cls.img = SimpleUploadedFile('img.jpg', b"file data")

        cls.comic = Comic.objects.create(
            title="One Piece",
            author="Eiichiro Oda",
            cover=cls.img
        )

        cls.review = Review.objects.create(
            comic=cls.comic,
            author=cls.user,
            review="An excellent review",
        )

    def test_comic_listing(self):
        self.assertEqual(f"{self.comic.title}", "One Piece")
        self.assertEqual(f"{self.comic.author}", "Eiichiro Oda")

    def test_comic_list_view_for_logged_in_user(self):
        self.client.login(email="reviewuser@email.com", password="testpass123")
        response = self.client.get(reverse("comic_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "One Piece")
        self.assertTemplateUsed(response, "comics/comic_list.html")

    def test_comic_list_view_for_logged_out_user(self):
        self.client.logout()
        response = self.client.get(reverse("comic_list"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, "%s?next=/comics/" % (reverse("account_login")))
        response = self.client.get(
            "%s?next=/comics/" % (reverse("account_login")))
        self.assertContains(response, "Log In")

    def test_comic_detail_view_with_permissions(self):
        self.client.login(email="reviewuser@email.com", password="testpass123")
        self.user.user_permissions.add(self.special_permission)
        response = self.client.get(self.comic.get_absolute_url())
        no_response = self.client.get("/comics/12345/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, "One Piece")
        self.assertContains(response, "An excellent review")
        self.assertTemplateUsed(response, "comics/comic_detail.html")