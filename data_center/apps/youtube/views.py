from django.shortcuts import render
from rest_framework import filters, viewsets
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin

from apps.youtube.models import Videos
from apps.youtube.serializers import VideosModelSerializer


class YoutubeViewSet(ListModelMixin, viewsets.GenericViewSet):

    http_method_names = ['get']
    permission_classes = []
    authentication_classes = []
    queryset = Videos.objects.all()
    serializer_class = VideosModelSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'description']
