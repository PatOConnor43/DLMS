from django.db.models import Q
from rest_framework import filters, status
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.viewsets import ModelViewSet, ViewSet

from .exceptions import DuplicateContentFileException
from .models import Content, Directory, DirectoryLayout, Tag
from .serializers import ContentSerializer, DirectoryLayoutSerializer, DirectorySerializer, TagSerializer
from .utils import FilterCriteriaUtil


class ContentApiViewset(ModelViewSet):
    queryset = Content.objects.all()
    serializer_class = ContentSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'description')

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except DuplicateContentFileException as dup:
            content_url = reverse('content-detail', args=[dup.content.pk], request=request)
            data = {
                'result': 'error',
                'error': 'DUPLICATE_FILE_UPLOADED',
                'existing_content': {
                    'content_url': content_url,
                    'file_url': request.build_absolute_uri(dup.content.content_file.url)
                }
            }
            return Response(data, status=status.HTTP_409_CONFLICT)

    def update(self, request, *args, **kwargs):
        try:
            return super().update(request, *args, **kwargs)
        except DuplicateContentFileException as dup:
            content_url = reverse('content-detail', args=[dup.content.pk], request=request)
            data = {
                'result': 'error',
                'error': 'DUPLICATE_FILE_UPLOADED',
                'existing_content': {
                    'content_url': content_url,
                    'file_url': request.build_absolute_uri(dup.content.content_file.url)
                }
            }
            return Response(data, status=status.HTTP_409_CONFLICT)


class TagViewSet(ModelViewSet):
    serializer_class = TagSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('description', 'name')

    def get_child(self, matching_result, tags_set):
        children = matching_result.child_tags.all()
        for child in children:
            tags_set.add(child)
            self.get_child(child, tags_set)

    def get_queryset(self):
        queryset = Tag.objects.all()
        search_param = self.request.query_params.get('search', None)
        if search_param is not None:
            queryset = queryset.filter(Q(name__icontains=search_param) | Q(description__icontains=search_param))
        return queryset

    def list(self, request, *args, **kwargs):
        tags_set = set()
        all_matches = self.get_queryset()
        include_subtags = self.request.query_params.get('subtags', False)
        for matching_result in all_matches:
            tags_set.add(matching_result)
            if include_subtags:
                self.get_child(matching_result, tags_set)
        serializer = self.get_serializer(tags_set, many=True)
        return Response(serializer.data)


class DirectoryLayoutViewSet(ModelViewSet):
    serializer_class = DirectoryLayoutSerializer
    queryset = DirectoryLayout.objects.all()


class DirectoryViewSet(ModelViewSet):
    serializer_class = DirectorySerializer
    queryset = Directory.objects.all()


class DirectoryCloneApiViewset(ViewSet, CreateModelMixin):
    serializer_class = DirectoryLayoutSerializer

    def create(self, request, *args, **kwargs):
        cloned_layout = self.get_queryset()
        clone = DirectoryLayout(name=cloned_layout.name + "_clone", description=cloned_layout.description)
        clone.pk = None
        clone.save()

        filter_criteria_obj = FilterCriteriaUtil()
        dir_queryset = Directory.objects.filter(dir_layout_id=cloned_layout.id)
        for dir in dir_queryset:
            dir.pk = None
            dir.dir_layout = clone
            cloned_filter_criteria_str = dir.filter_criteria.get_filter_criteria_string()
            dir.filter_criteria = filter_criteria_obj.create_filter_criteria_from_string(cloned_filter_criteria_str)
            dir.save()

        serializer = DirectoryLayoutSerializer(clone)
        return Response(serializer.data)

    def get_queryset(self, **kwargs):
        queryset = DirectoryLayout.objects.get(id=self.kwargs['id'])
        return queryset
