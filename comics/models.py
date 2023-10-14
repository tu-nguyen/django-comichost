import os
import uuid
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django_project.settings import MEDIA_URL



def generate_comic_path(instance, filename):
    clean_filename = os.path.basename(filename)
    if isinstance(instance, Comic):
        comic_id = str(instance.id)
        sub_folder = "cover"

    else:
        comic_id = str(instance.chapter.comic.id)
        sub_folder = str(instance.chapter)

    return os.path.join(MEDIA_URL, comic_id, sub_folder, clean_filename)
    



class Comic(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    cover = models.ImageField(upload_to=generate_comic_path, blank=True)
    uploader = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        null=True
    )

    class Meta:
        indexes = [
            models.Index(fields=["id"], name="id_index"),
        ]
        permissions = [
            ("special_status", "Can read all comics"),
        ]

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("comic_detail", args=[str(self.id)])
    
    def get_chapters_absolute_url(self):
        return reverse("chapter_list", args=[str(self.id)])
    
    


class ComicChapter(models.Model):
    chapter = models.IntegerField()
    title = models.CharField(max_length=200)
    comic = models.ForeignKey(
        Comic,
        on_delete=models.CASCADE,
        related_name="pages",
    )

    class Meta:
        indexes = [
            models.Index(fields=["comic", "chapter"], name="comic_chapter_index"),
        ]
        constraints = [
            models.UniqueConstraint(fields=["comic", "chapter"], name="unique_comic_chapter")
        ]
        ordering = ["chapter"]

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("chapter_detail", args=[str(self.comic.id), str(self.chapter)])
    
    def get_first_page_absolute_url(self):
        if first_page := ComicPage.objects.filter(chapter=self).order_by("page").values_list(flat=True).first():
            return reverse("page_list", args=[str(self.comic.id), str(self.chapter)])
        else:
            return ""
    



class ComicPage(models.Model):
    page = models.IntegerField()
    chapter = models.ForeignKey(
        ComicChapter,
        on_delete=models.CASCADE,
        related_name="chapters",
    )
    img = models.ImageField(upload_to=generate_comic_path, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=["chapter", "page"], name="chapter_page_index"),
        ]
        constraints = [
            models.UniqueConstraint(fields=["chapter", "page"], name="unique_chapter_page")
        ]

    def get_absolute_url(self):
        return reverse("page_detail", args=[str(self.chapter.comic.id), str(self.chapter.chapter), str(self.page)])

    

class Review(models.Model):
    comic = models.ForeignKey(
        Comic,
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    review = models.CharField(max_length=255)
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.review