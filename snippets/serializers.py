import logging

from django.contrib.auth.models import User
from keyring.backends import null
from rest_framework import serializers

from snippets.models import LANGUAGE_CHOICES, STYLE_CHOICES, OutFit, Person, Snippet

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


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
        exclude = ["persons"]


class PersonSerializer(serializers.ModelSerializer):
    outfits = OutFitSerializer(many=True, source="outfit_set", required=False)

    class Meta:
        model = Person
        exclude = ["created_at", "updated_at"]

    def create(self, validated_data):
        outfits_data = validated_data.pop("outfit_set", [])
        person = Person.objects.create(**validated_data)
        for outfit_data in outfits_data:
            outfit = OutFit.objects.create(**outfit_data)
            outfit.persons.add(person)
        return person

    def update(self, instance, validated_data):
        outfits_data = validated_data.pop("outfit_set", None)

        # Update the person fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update outfits if provided
        if outfits_data is not None:
            logger.info("In Outfit clearing area.")
            instance.outfit_set.clear()
            for outfit_data in outfits_data:
                outfit = OutFit.objects.create(**outfit_data)
                outfit.persons.add(instance)

        return instance

    def partial_update(self, instance, validated_data):
        logger.info("In Partial Update Area.")
        outfits_data = validated_data.pop("outfit_set", None)
        print(outfits_data)

        # Update the person fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update outfits if provided
        if outfits_data is not None:
            instance.outfit_set.clear()
            for outfit_data in outfits_data:
                outfit = OutFit.objects.create(**outfit_data)
                outfit.persons.add(instance)

        return instance
