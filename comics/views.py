from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)
from django.db.models import Q
from django.views.generic import ListView, DetailView
from .models import Comic, ComicChapter, ComicPage



class ComicListView(LoginRequiredMixin, ListView):
    model = Comic
    context_object_name = "comic_list"
    template_name = "comics/comic_list.html"
    login_url = "account_login"


class ComicDetailView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    DetailView):
    model = Comic
    context_object_name = "comic"
    template_name = "comics/comic_detail.html"
    login_url = "account_login"
    permission_required = "comics.special_status"


class SearchResultslistView(ListView):
    model = Comic
    context_object_name = "comic_list"
    template_name = "comics/search_results.html"
    
    def get_queryset(self):
        query = self.request.GET.get("q")
        return Comic.objects.filter(
            Q(title__icontains=query) | Q(author__icontains=query)
        )
    

class ChapterListView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    ListView):
    model = ComicChapter
    context_object_name = "chapter_list"
    template_name = "comics/chapter_list.html"
    login_url = "account_login"
    permission_required = "comics.special_status"

    def get_queryset(self):
        comic = Comic.objects.get(id=self.kwargs.get("comic_id"))

        return ComicChapter.objects.filter(comic=comic)


class ChapterDetailView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    DetailView):
    model = ComicChapter
    context_object_name = "chapter"
    template_name = "comics/chapter_detail.html"
    login_url = "account_login"
    permission_required = "comics.special_status"
    queryset = Comic.objects.all().prefetch_related("review_author",)

class PageListView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    ListView):
    model = ComicPage
    context_object_name = "page_list"
    template_name = "comics/comic_page.html"
    login_url = "account_login"
    permission_required = "comics.special_status"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_chapter = self.kwargs.get("chapter_id")
        context["chapter"] = current_chapter

        comic = Comic.objects.get(id=self.kwargs.get("comic_id"))
        
        try:
            context["previous_chapter"] = ComicChapter.objects.get(comic=comic, chapter=current_chapter-1)
        except ComicChapter.DoesNotExist:
            context["previous_chapter"] = ""
            
        try:
            context["next_chapter"] = ComicChapter.objects.get(comic=comic, chapter=current_chapter+1)
        except ComicChapter.DoesNotExist:
            context["next_chapter"] = ""
       
        return context

    def get_queryset(self):
        return ComicPage.objects.filter(chapter__id=self.kwargs.get("chapter_id"))