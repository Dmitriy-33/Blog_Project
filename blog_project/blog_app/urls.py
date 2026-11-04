
from django.urls import path, re_path
from . import views

app_name = "blog_app"

urlpatterns = [
    path("", views.PostListView.as_view(), name="post_list"),
    re_path(
        r"^(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/(?P<slug>[\w-]+)/$",
        views.PostDetailView.as_view(),
        name="post_detail",
    ),
    path("create/", views.PostCreateView.as_view(), name="post_create"),
    re_path(
        r"^(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/(?P<slug>[\w-]+)/update/$",
        views.PostUpdateView.as_view(),
        name="post_update",
    ),
    re_path(
        r"^(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/(?P<slug>[\w-]+)/delete/$",
        views.PostDeleteView.as_view(),
        name="post_delete",
    ),
    re_path(
        r"^(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/(?P<slug>[\w-]+)/comment/$",
        views.add_comment,
        name="add_comment",
    ),
]
