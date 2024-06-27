# urls.py
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns

from snippets import views

app_name = "snippets"

router = DefaultRouter()
router.register(r"persons", views.PersonViewSet)
router.register(r"outfits", views.OutFitViewSet)

urlpatterns = [
    path("snippets/", views.Snippet_list.as_view(), name="snippet-list"),
    path("snippets/<int:pk>/", views.Snippet_detail.as_view(), name="snippet-detail"),
    path(
        "snippets/<int:pk>/highlight/",
        views.SnippetHighlight.as_view(),
        name="snippet-highlight",
    ),
    path("users/", views.UserList.as_view(), name="user-list"),
    path("users/<int:pk>/", views.UserDetail.as_view(), name="user-detail"),
    # path("persons/", views.Person_list.as_view(), name="person-list"),
    path("", include(router.urls)),
]

# urlpatterns = format_suffix_patterns(urlpatterns)
