from django.contrib.auth.models import User
from rest_framework import serializers

from snippets.models import LANGUAGE_CHOICES, STYLE_CHOICES, Person, Snippet


class SnippetSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")
    highlight = serializers.HyperlinkedIdentityField(
        view_name="snippets:snippet-highlight", format="html"
    )
    url = serializers.HyperlinkedIdentityField(
        view_name="snippets:snippet-detail"
    )  # Ensure the view_name is correct

    class Meta:
        model = Snippet
        fields = [
            "url",
            "id",
            "title",
            "code",
            "linenos",
            "language",
            "style",
            "owner",
            "highlight",
        ]


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = [
            "id",
            "first_name",
            "last_name",
            "title",
            "is_married",
            "is_programmer",
        ]


class UserSerializer(serializers.HyperlinkedModelSerializer):
    snippets = serializers.HyperlinkedRelatedField(
        many=True, view_name="snippets:snippet-detail", read_only=True
    )

    class Meta:
        model = User
        fields = ["url", "id", "username", "snippets"]
        extra_kwargs = {"url": {"view_name": "snippets:user-detail"}}
