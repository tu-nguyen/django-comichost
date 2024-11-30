# coding=utf-8
"""
Backfill for testing
"""
import os
from io import BytesIO
from PIL import Image
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management.base import BaseCommand
from comics.models import Comic, ComicChapter, ComicPage, Review


def create_comic_contents(self, comic, chapter_pages, dummy_pages):
    for chapter, chapter_data in enumerate(chapter_pages, start=1):
        if not ComicChapter.objects.filter(comic=comic, chapter=chapter).exists():
            comic_chapter = ComicChapter.objects.create(
                chapter=chapter,
                title=chapter_data["title"],
                comic=comic,
            )
            if self:
                self.stdout.write(
                    self.style.SUCCESS(f"Dummy Chapter {chapter} created for {comic.title}")
                )

        else:
            comic_chapter = ComicChapter.objects.get(
                chapter=chapter,
                comic=comic,
            )
            if self:
                self.stdout.write(
                    self.style.SUCCESS(f"Dummy Chapter {chapter} for {comic.title} already exists")
                )

        for i in range(1, chapter_data["pages"] + 1, 1):
            if not ComicPage.objects.filter(page=i, chapter=comic_chapter).exists():
                image = Image.open(BytesIO(dummy_pages[i - 1]))
                image.thumbnail((800, 600))

                output = BytesIO()
                image.save(output, format='JPEG', quality=85)
                image_data = output.getvalue()

                page = ComicPage.objects.create(
                    chapter=comic_chapter,
                    page=i,
                )
                if self:
                    self.stdout.write(
                        self.style.SUCCESS(f"Dummy Page created {i} for {comic.title}'s chapter {comic_chapter}")
                    )

                with open(f"/tmp/{comic.title.replace(' ', '-')}-{comic_chapter.chapter}-{i}.jpg", "wb") as f:
                    f.write(image_data)

                reopen = open(f"/tmp/{comic.title.replace(' ', '-')}-{comic_chapter.chapter}-{i}.jpg", "rb")
                django_file = File(reopen)

                page.img.save(f"{i}.jpg", django_file, save=True)


def generate_reviews(self, comic, review_list):
    for review_dict in review_list:
        Review.objects.create(
                comic=comic,
                author=review_dict["author"],
                review=review_dict["review"],
            )
        if self:
            self.stdout.write(
                self.style.SUCCESS(f"Review created for {comic.title} with author {review_dict['author']}")
            )


class Command(BaseCommand):
    """
    Command to backfill with dummy data
    """

    def add_arguments(self, parser):
        """
        Add args
        Args:
            parser ():
        """

    def handle(self, *args, **kwargs):
        """
        Run
        Args:
            *args ():
            **kwargs ():

        Returns:

        """
        self.stdout.write(
            self.style.NOTICE("Backfilling Dummy Users")
        )

        User = get_user_model()

        user_dict = {
            "testuser1": {
                "username": "testuser1",
                "email": "testuser1@email.com",
                "password": "testpass1",
            },
            "testuser2": {
                "username": "testuser2",
                "email": "testuser2@email.com",
                "password": "testpass2",
            },
            "testuser3": {
                "username": "testuser3",
                "email": "testuser3@email.com",
                "password": "testpass3",
            },  
        }
        users = []
        for user, user_data in user_dict.items():
            if not User.objects.filter(username=user).exists():
                curr_user = User.objects.create_user(
                    username=user_data["username"],
                    email=user_data["email"],
                    password=user_data["password"],
                )
                self.stdout.write(
                    self.style.SUCCESS("Successfully created user: '%s'" % curr_user)
                )
            else:
                curr_user = User.objects.get(username=user)
                self.stdout.write(
                    self.style.SUCCESS("User already exists: '%s'" % curr_user)
                )
            
            users.append(curr_user)

        special_permission = Permission.objects.get(
            codename="special_status"
        )
        for user in users:
            user.user_permissions.add(special_permission)
            self.stdout.write(
                self.style.SUCCESS("User ready: '%s'" % user)
            )

        self.stdout.write(
            self.style.SUCCESS("Backfilling Dummy Users Completed!")
        )

        self.stdout.write(
            self.style.NOTICE("Backfilling Dummy Comics")
        )

        dirname = os.path.dirname(__file__)

        # Comic 1
        if not Comic.objects.filter(title="One Piece").exists():
            filename = os.path.join(dirname, '../../../static\images\op_cover.jpg')

            with open(filename, 'rb') as infile:
                op_img = SimpleUploadedFile(filename, infile.read())

                Comic.objects.create(
                    title="One Piece",
                    author="Eiichiro Oda",
                    cover=op_img,
                    uploader=users[2],
                )
            self.stdout.write(
                self.style.SUCCESS("Successfully created comic: One Piece")
            )

        # Comic 2
        if not Comic.objects.filter(title="My Hero Academia").exists():
            filename = os.path.join(dirname, '../../../static\images\hero_aka_cover.jpg')

            with open(filename, 'rb') as infile:
                hero_aka_img = SimpleUploadedFile(filename, infile.read())

                Comic.objects.create(
                    title="My Hero Academia",
                    author="Kohei Horikoshi",
                    cover=hero_aka_img,
                    uploader=users[1],
                )

        self.stdout.write(
            self.style.SUCCESS("Successfully backfilled: My Hero Academia")
        )

        self.stdout.write(
            self.style.SUCCESS("Backfilling Dummy Comics Completed!")
        )

        self.stdout.write(
            self.style.NOTICE("Backfilling Dummy Chapters and Pages")
        )
        # page1 = Image.open(os.path.join(dirname, '../../../static\images\\1.jpg'))
        # page2 = Image.open(os.path.join(dirname, '../../../static\images\\2.jpg'))
        # page3 = Image.open(os.path.join(dirname, '../../../static\images\\3.jpg'))
        # page4 = Image.open(os.path.join(dirname, '../../../static\images\\4.jpg'))
        with open(os.path.join(dirname, '../../../static\images\\1.jpg'), 'rb') as fd1:
            page1 = fd1.read()
        with open(os.path.join(dirname, '../../../static\images\\2.jpg'), 'rb') as fd2:
            page2 = fd2.read()
        with open(os.path.join(dirname, '../../../static\images\\3.jpg'), 'rb') as fd3:
            page3 = fd3.read()
        with open(os.path.join(dirname, '../../../static\images\\4.jpg'), 'rb') as fd4:
            page4 = fd4.read()

        dummy_pages = [page1, page2, page3, page4]
        self.stdout.write(
            self.style.NOTICE("Dummy Pages Prep")
        )

        op_comic = Comic.objects.get(title="One Piece")
        one_piece_chapter_page_dict = [
            {"title": "chapter 1", "pages": 4},
            {"title": "chapter 2", "pages": 3},
            {"title": "chapter 3", "pages": 4},
            {"title": "chapter 4", "pages": 3},
        ]
        create_comic_contents(self, op_comic, one_piece_chapter_page_dict, dummy_pages)

        hero_aka_comic = Comic.objects.get(title="My Hero Academia")
        hero_aka_chapter_page_dict = [
            {"title": "chapter 1", "pages": 3},
            {"title": "chapter 2", "pages": 3},
            {"title": "chapter 3", "pages": 2},
        ]
        create_comic_contents(self, hero_aka_comic, hero_aka_chapter_page_dict, dummy_pages)

        self.stdout.write(
            self.style.SUCCESS("Backfilling Dummy Chapters and Pages Completed!")
        )

        self.stdout.write(
            self.style.NOTICE("Backfilling Dummy Reviews")
        )

        review_dict = {
            op_comic: [
                {
                    "author": users[1],
                    "review": "This is too long"
                },
                {
                    "author": users[2],
                    "review": "Nothing more incorrect"
                },
                {
                    "author": users[1],
                    "review": "You right, it ain't long enough"
                },

            ],
            hero_aka_comic: [
                {
                    "author": users[2],
                    "review": "zzzz"
                },
                {
                    "author": users[1],
                    "review": "meh"
                },
            ],
        }

        for comic, comic_review in review_dict.items():
            generate_reviews(self, comic, comic_review)

        self.stdout.write(
            self.style.SUCCESS("Backfilling Dummy Reviews Completed!")
        )

        self.stdout.write(
            self.style.HTTP_INFO("Project is ready, please runserver and use the below credentials to login\n")
        )
        self.stdout.write(
            self.style.HTTP_INFO("E-mail: testuser1@email.com")
        )
        self.stdout.write(
            self.style.HTTP_INFO("Password: testpass1")
        )