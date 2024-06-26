from django.contrib.auth.models import User
from keyring.backends import null
from rest_framework import serializers

from snippets.models import LANGUAGE_CHOICES, STYLE_CHOICES, OutFit, Person, Snippet


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


class UserSerializer(serializers.HyperlinkedModelSerializer):
    snippets = serializers.HyperlinkedRelatedField(
        many=True, view_name="snippets:snippet-detail", read_only=True
    )

    class Meta:
        model = User
        fields = ["url", "id", "username", "snippets"]
        extra_kwargs = {"url": {"view_name": "snippets:user-detail"}}


class OutFitSerializer(serializers.ModelSerializer):
    class Meta:
        model = OutFit
        fields = ["id", "upper_half", "lower_half", "footwear", "specs"]


class PersonSerializer(serializers.ModelSerializer):
    outfits = OutFitSerializer(many=True, read_only=True, source="outfit_set")

    class Meta:
        model = Person
        fields = [
            "id",
            "first_name",
            "last_name",
            "title",
            "is_married",
            "is_programmer",
            "outfits",
        ]

    def create(self, validated_data):
        outfits_data = validated_data.pop("outfits", [])
        person = Person.objects.create(**validated_data)
        for outfit_data in outfits_data:
            OutFit.objects.create(person=person, **outfit_data)
        return person
