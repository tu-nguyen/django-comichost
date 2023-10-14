from django.urls import path

from .views import ComicListView, ComicDetailView, SearchResultslistView, ChapterListView, ChapterDetailView, PageListView


urlpatterns = [
    path("", ComicListView.as_view(), name="comic_list"),
    path("<uuid:pk>/", ComicDetailView.as_view(), name="comic_detail"),
    path("search/", SearchResultslistView.as_view(), name="search_results"),
    path("<uuid:comic_id>/chapters/", ChapterListView.as_view(), name="chapter_list"),
    path("<uuid:comic_id>/ch-<int:pk>/", ChapterDetailView.as_view(), name="chapter_detail"),
    path("<uuid:comic_id>/ch-<int:chapter_id>/pages", PageListView.as_view(), name="page_list"),
]