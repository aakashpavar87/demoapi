import logging

from django.contrib.auth.models import User
from rest_framework import generics, mixins, renderers, status, viewsets
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from snippets.models import OutFit, Person, Snippet
from snippets.permissions import IsOwnerOrReadonly
from snippets.serializers import (
    OutFitSerializer,
    PersonSerializer,
    SnippetSerializer,
    UserSerializer,
)

logger = logging.getLogger(__name__)


class Snippet_list(generics.ListCreateAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadonly]

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(owner=self.request.user)
            logger.info("Snippet created successfully.")
        else:
            logger.error(f"Snippet creation failed: {serializer.errors}")


class Snippet_detail(generics.RetrieveUpdateDestroyAPIView):

    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadonly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs, partial=True)


# class Person_list(
#     mixins.CreateModelMixin, mixins.ListModelMixin, generics.GenericAPIView
# ):
class Person_list(generics.ListCreateAPIView):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def partial_update(self, request, *args, **kwargs):
        kwargs["partial"] = True
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, "_prefetched_objects_cache", None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


class OutFitViewSet(viewsets.ModelViewSet):
    queryset = OutFit.objects.all()
    serializer_class = OutFitSerializer

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


@api_view(["GET"])
def api_root(request, format=None):
    return Response(
        {
            "users": reverse("snippets:user-list", request=request, format=format),
            "snippets": reverse(
                "snippets:snippet-list", request=request, format=format
            ),
        }
    )


class SnippetHighlight(generics.GenericAPIView):
    queryset = Snippet.objects.all()
    renderer_classes = [renderers.StaticHTMLRenderer]

    def get(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)


# class Person_detail(
#     mixins.RetrieveModelMixin,
#     mixins.DestroyModelMixin,
#     mixins.UpdateModelMixin,
#     generics.GenericAPIView,
# ):
# class Person_detail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Person.objects.all()
#     serializer_class = PersonSerializer

#     # def get(self, request, *args, **kwargs):
#     #     return self.retrieve(request, *args, **kwargs)

#     def patch(
#         self,
#         request,
#         *args,
#         **kwargs,
#     ):
#         return self.update(request, *args, **kwargs, partial=True)

# def delete(self, request, *args, **kwargs):
#     return self.destroy(request, *args, **kwargs)


# Create your views here.
# class Snippet_list(APIView):
#     def get(self, formate=None):
#         snippets = Snippet.objects.all()
#         serializer = SnippetSerializer(snippets, many=True)
#         return Response(serializer.data)

#     def post(self, request, formate=None):
#         data = JSONParser().parse(request)
#         serializer = SnippetSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class Snippet_detail(APIView):
#     def get_object(self, pk, format=None):
#         """
#         Retrieve, update or delete a code snippet.
#         """
#         try:
#             self.snippet = Snippet.objects.get(pk=pk)
#         except Snippet.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)

#     def get(self, pk, format=None):
#         serializer = SnippetSerializer(self.snippet)
#         return Response(serializer.data)

#     def put(self, request, pk, format=None):
#         data = JSONParser().parse(request)
#         serializer = SnippetSerializer(self.snippet, data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, format=None):
#         self.snippet.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# class Person_list(APIView):
#     def get(self, format=None):
#         persons = Person.objects.all()
#         serializer = PersonSerializer(persons, many=True)
#         return Response(serializer.data)

#     def post(self, request, format=None):
#         data = JSONParser().parse(request)
#         serializer = PersonSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class Person_detail(APIView):
#     def get_object(self, pk):
#         try:
#             self.person = Person.objects.get(pk=pk)
#         except Person.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)

#     def get(self):
#         serializer = PersonSerializer(self.person)
#         return Response(serializer.data)

#     def patch(self, request):
#         data = JSONParser().parse(request)
#         serializer = PersonSerializer(self.person, data=data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class Snippet_list(
#     mixins.CreateModelMixin, mixins.ListModelMixin, generics.GenericAPIView
# ):
#     queryset = Snippet.objects.all()
#     serializer_class = SnippetSerializer

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)


# class Snippet_detail(
#     mixins.RetrieveModelMixin,
#     mixins.DestroyModelMixin,
#     mixins.UpdateModelMixin,
#     generics.GenericAPIView,
# ):
#     queryset = Snippet.objects.all()
#     serializer_class = SnippetSerializer

#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)

#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs, partial=True)

#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)
