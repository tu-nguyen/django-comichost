from django.contrib import admin
from .models import Comic, Review, ComicChapter, ComicPage



class ReviewInline(admin.TabularInline):
    model = Review

class ComicChapterInline(admin.TabularInline):
    model = ComicChapter

class ComicAdmin(admin.ModelAdmin):
    inlines = [
        ComicChapterInline,
        ReviewInline,
    ]
    list_display = ("title", "author", "uploader")


admin.site.register(Comic, ComicAdmin)

    

class ComicPageInline(admin.TabularInline):
    model = ComicPage

class ChapterAdmin(admin.ModelAdmin):
    inlines = [
        ComicPageInline,
    ]
    list_display = ("chapter", "title", "comic")

admin.site.register(ComicChapter, ChapterAdmin)

