# urls.py
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from snippets import views

app_name = "snippets"

urlpatterns = [
    path("", views.api_root),
    path("snippets/", views.Snippet_list.as_view(), name="snippet-list"),
    path("snippets/<int:pk>/", views.Snippet_detail.as_view(), name="snippet-detail"),
    path(
        "snippets/<int:pk>/highlight/",
        views.SnippetHighlight.as_view(),
        name="snippet-highlight",
    ),
    path("users/", views.UserList.as_view(), name="user-list"),
    path("users/<int:pk>/", views.UserDetail.as_view(), name="user-detail"),
    path("persons/", views.Person_list.as_view(), name="person-list"),
    path("persons/<int:pk>/", views.Person_detail.as_view(), name="person-detail"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
