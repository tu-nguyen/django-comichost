"""Test the manage.py backfill_dummy management command"""
import os
from io import BytesIO, StringIO
from PIL import Image

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management import call_command
from django.test import TestCase

from comics.models import Comic, ComicChapter, ComicPage, Review
from comics.management.commands.backfill_dummy import create_comic_contents, generate_reviews
from unittest.mock import patch


class TestBackfillDummyCommand(TestCase):

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

    def test_create_comic_contents_success(self):
        test_comic1 = Comic.objects.create(
            title="Comic 1",
            author="Author 1",
            cover=self.img,
            uploader=self.user,
        )

        chapter_page_dict = [
            {"title": "chapter 1", "pages": 4},
            {"title": "chapter 2", "pages": 3},
            {"title": "chapter 3", "pages": 4},
            {"title": "chapter 4", "pages": 3},
        ]

        dirname = os.path.dirname(__file__)
        with open(os.path.join(dirname, '../../../static\images\\1.jpg'), 'rb') as fd1:
            page1 = fd1.read()
        with open(os.path.join(dirname, '../../../static\images\\2.jpg'), 'rb') as fd2:
            page2 = fd2.read()
        with open(os.path.join(dirname, '../../../static\images\\3.jpg'), 'rb') as fd3:
            page3 = fd3.read()
        with open(os.path.join(dirname, '../../../static\images\\4.jpg'), 'rb') as fd4:
            page4 = fd4.read()

        dummy_pages = [page1, page2, page3, page4]

        create_comic_contents(None, test_comic1, chapter_page_dict, dummy_pages)

        chapters = ComicChapter.objects.filter(comic=test_comic1)
        self.assertEqual(len(chapters), len(chapter_page_dict))
        for i, chapter in enumerate(chapters, start=1):
            self.assertEqual(chapter.chapter, i)
            self.assertEqual(chapter.title, chapter_page_dict[i-1]["title"])

            pages = ComicPage.objects.filter(chapter=chapter)
            for i, page in enumerate(pages, start=1):
                self.assertEqual(page.page, i)

    def test_generate_reviews(self):
        User = get_user_model()
        user = User.objects.create_user(
            username="test", email="test@gmail.com", password="test"
        )

        test_comic1 = Comic.objects.create(
            title="Comic 1",
            author="Author 1",
            cover=self.img,
            uploader=self.user,
        )
        
        review_list = [
            {
                "author": user,
                "review": "comment 1"
            },
            {
                "author": user,
                "review": "comment 2"
            },
            {
                "author": user,
                "review": "comment 3"
            },

        ]

        generate_reviews(None, test_comic1, review_list)

        reviews = Review.objects.all()
        self.assertEqual(len(reviews), 3)
        for i, review in enumerate(reviews, start=1):
            self.assertEqual(review.comic, test_comic1)
            self.assertEqual(review.review, f"comment {i}")
            self.assertEqual(review.author, user)

    def test_backfill_success(self):
        out = StringIO()
        call_command("backfill_dummy", stdout=out)

        comics = Comic.objects.all().order_by("date_uploaded")
        self.assertEqual(len(comics), 2)
        comic1 = comics[0]
        self.assertEqual(comic1.title, "One Piece")
        comic2 = comics[1]
        self.assertEqual(comic2.title, "My Hero Academia")

        reviews = Review.objects.all().order_by("date_uploaded")
        self.assertEqual(len(reviews), 5)

        self.assertIn("Backfilling Dummy Users Completed!", out.getvalue())
        self.assertIn("Backfilling Dummy Comics Completed!", out.getvalue())
        self.assertIn("Backfilling Dummy Chapters and Pages Completed!", out.getvalue())
        self.assertIn("Backfilling Dummy Reviews Completed!", out.getvalue())
