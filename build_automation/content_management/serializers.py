from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from content_management.models import (
    Cataloger, Content, Coverage, Creator, Directory, DirectoryLayout, Keyword, Language, Subject, Workarea
)


class ContentSerializer(serializers.ModelSerializer):

    creators = serializers.PrimaryKeyRelatedField(many=True, queryset=Creator.objects.all(), read_only=False)
    coverage = serializers.PrimaryKeyRelatedField(
        queryset=Coverage.objects.all(), read_only=False, allow_null=True, required=False
    )
    subjects = serializers.PrimaryKeyRelatedField(many=True, queryset=Subject.objects.all(), read_only=False)
    keywords = serializers.PrimaryKeyRelatedField(many=True, queryset=Keyword.objects.all(), read_only=False)
    workareas = serializers.PrimaryKeyRelatedField(many=True, queryset=Workarea.objects.all(), read_only=False)
    language = serializers.PrimaryKeyRelatedField(
        queryset=Language.objects.all(), read_only=False, allow_null=True, required=False
    )
    cataloger = serializers.PrimaryKeyRelatedField(
        queryset=Cataloger.objects.all(), read_only=False, allow_null=True, required=False
    )

    def create(self, validated_data):
        validated_data_copy = dict(validated_data)
        del validated_data_copy['creators']
        del validated_data_copy['subjects']
        del validated_data_copy['keywords']
        del validated_data_copy['workareas']
        content = Content(**validated_data_copy)
        content = self.__create_update(content, None)
        content.creators.set(validated_data['creators'])
        content.subjects.set(validated_data['subjects'])
        content.keywords.set(validated_data['keywords'])
        content.workareas.set(validated_data['workareas'])
        content.save()
        return content

    def update(self, content, validated_data):
        content.name = validated_data.get('name', content.name)
        content.description = validated_data.get('description', content.description)
        content.content_file = validated_data.get('content_file', content.content_file)
        content.creators.set(validated_data.get('creators', content.creators.all()))
        content.coverage = (validated_data.get('coverage', content.coverage))
        content.subjects.set(validated_data.get('subjects', content.subjects.all()))
        content.keywords.set(validated_data.get('keywords', content.keywords.all()))
        content.workareas.set(validated_data.get('workareas', content.workareas.all()))
        content.language = (validated_data.get('language', content.language))
        content.cataloger = (validated_data.get('cataloger', content.cataloger))

        return self.__create_update(content)

    def __create_update(self, content, tag_list=None):
        request = self.context['request']
        if 'content_file' in request.FILES:
            content.content_file_uploaded = True
        content.save()
        return content

    class Meta:
        model = Content
        fields = ('url', 'id', 'name', 'description', 'content_file', 'updated_time', 'last_uploaded_time', 'creators',
                  'coverage', 'subjects', 'keywords', 'workareas', 'language', 'cataloger')
        extra_kwargs = {
            'url': {'lookup_field': 'pk'},
        }


class CreatorSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        max_length=50, validators=[
            UniqueValidator(
                queryset=Creator.objects.all(),
                message={
                    'error': 'DUPLICATE_CREATOR_NAME'
                },
                lookup='iexact'
            )
        ]
    )

    class Meta:
        model = Creator
        fields = ('id', 'url', 'name', 'description')
        extra_kwargs = {
            'url': {'lookup_field': 'pk'},
        }


class CoverageSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        max_length=50, validators=[
            UniqueValidator(
                queryset=Coverage.objects.all(),
                message={
                    'error': 'DUPLICATE_COVERAGE_NAME'
                },
                lookup='iexact'
            )
        ]
    )

    class Meta:
        model = Coverage
        fields = ('id', 'url', 'name', 'description')
        extra_kwargs = {
            'url': {'lookup_field': 'pk'},
        }


class SubjectSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        max_length=50, validators=[
            UniqueValidator(
                queryset=Subject.objects.all(),
                message={
                    'error': 'DUPLICATE_SUBJECT_NAME'
                },
                lookup='iexact'
            )
        ]
    )

    class Meta:
        model = Subject
        fields = ('id', 'url', 'name', 'description')
        extra_kwargs = {
            'url': {'lookup_field': 'pk'},
        }


class KeywordSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        max_length=50, validators=[
            UniqueValidator(
                queryset=Keyword.objects.all(),
                message={
                    'error': 'DUPLICATE_KEYWORD_NAME'
                },
                lookup='iexact'
            )
        ]
    )

    class Meta:
        model = Keyword
        fields = ('id', 'url', 'name', 'description')
        extra_kwargs = {
            'url': {'lookup_field': 'pk'},
        }


class WorkareaSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        max_length=50, validators=[
            UniqueValidator(
                queryset=Workarea.objects.all(),
                message={
                    'error': 'DUPLICATE_WORKAREA_NAME'
                },
                lookup='iexact'
            )
        ]
    )

    class Meta:
        model = Workarea
        fields = ('id', 'url', 'name', 'description')
        extra_kwargs = {
            'url': {'lookup_field': 'pk'},
        }


class LanguageSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        max_length=50, validators=[
            UniqueValidator(
                queryset=Language.objects.all(),
                message={
                    'error': 'DUPLICATE_LANGUAGE'
                },
                lookup='iexact'
            )
        ]
    )

    class Meta:
        model = Language
        fields = ('id', 'url', 'name', 'description')
        extra_kwargs = {
            'url': {'lookup_field': 'pk'},
        }


class CatalogerSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        max_length=50, validators=[
            UniqueValidator(
                queryset=Cataloger.objects.all(),
                message={
                    'error': 'DUPLICATE_CATALOGER_NAME'
                },
                lookup='iexact'
            )
        ]
    )

    class Meta:
        model = Cataloger
        fields = ('id', 'url', 'name', 'description')
        extra_kwargs = {
            'url': {'lookup_field': 'pk'},
        }


class DirectoryLayoutSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        max_length=50,
        validators=[
            UniqueValidator(
                queryset=DirectoryLayout.objects.all(),
                message=('DUPLICATE_LAYOUT_NAME')
            )
        ]
    )

    def create(self, validated_data):
        dir_layout = DirectoryLayout(**validated_data)
        dir_layout = self.__create_update(dir_layout)
        return dir_layout

    def update(self, dir_layout, validated_data):
        dir_layout.name = validated_data.get('name', dir_layout.name)
        dir_layout.description = validated_data.get('description', dir_layout.description)
        dir_layout.banner_file = validated_data.get('banner_file', dir_layout.banner_file)
        return self.__create_update(dir_layout)

    def __create_update(self, dir_layout):
        request = self.context['request']
        if 'banner_file' in request.FILES:
            dir_layout.banner_file_uploaded = True
        dir_layout.save()
        return dir_layout

    class Meta:
        model = DirectoryLayout
        fields = ('id', 'url', 'name', 'description', 'banner_file', 'original_file_name')
        read_only_fields = ('original_file_name',)
        extra_kwargs = {
            'url': {'lookup_field': 'pk'},
        }


class DirectoryNameUniqueValidator(object):
    def __call__(self, directory):
        dir_name = directory.get('name')
        parent = directory.get('parent')
        dir_layout = directory.get('dir_layout')
        if self.id is None:
            matching_dirs_count = Directory.objects.filter(
                dir_layout=dir_layout, parent=parent, name__iexact=dir_name
            ).count()
        else:
            matching_dirs_count = Directory.objects.filter(
                dir_layout=dir_layout, parent=parent, name__iexact=dir_name
            ).exclude(pk=self.id).count()
        if matching_dirs_count > 0:
            raise serializers.ValidationError({'name': [{'result': 'ERROR', 'error': 'DUPLICATE_DIRECTORY'}]})

    def set_context(self, serializer_field):
        self.id = serializer_field.initial_data.get('id')


class DirectorySerializer(serializers.ModelSerializer):
    """
    Create and Update functions to override the value of filter_criteria
    """

    individual_files = serializers.PrimaryKeyRelatedField(many=True, queryset=Content.objects.all(), read_only=False)
    creators = serializers.PrimaryKeyRelatedField(many=True, queryset=Creator.objects.all(), read_only=False)
    coverages = serializers.PrimaryKeyRelatedField(many=True, queryset=Coverage.objects.all(), read_only=False)
    subjects = serializers.PrimaryKeyRelatedField(many=True, queryset=Subject.objects.all(), read_only=False)
    keywords = serializers.PrimaryKeyRelatedField(many=True, queryset=Keyword.objects.all(), read_only=False)
    workareas = serializers.PrimaryKeyRelatedField(many=True, queryset=Workarea.objects.all(), read_only=False)
    languages = serializers.PrimaryKeyRelatedField(many=True, queryset=Language.objects.all(), read_only=False)
    catalogers = serializers.PrimaryKeyRelatedField(many=True, queryset=Cataloger.objects.all(), read_only=False)

    def create(self, validated_data):
        validated_data_copy = dict(validated_data)
        del validated_data_copy['individual_files']
        del validated_data_copy['creators']
        del validated_data_copy['coverages']
        del validated_data_copy['subjects']
        del validated_data_copy['keywords']
        del validated_data_copy['workareas']
        del validated_data_copy['languages']
        del validated_data_copy['catalogers']
        directory = Directory(**validated_data_copy)
        self.__create_update(directory)
        directory.individual_files.set(validated_data['individual_files'])
        directory.creators.set(validated_data['creators'])
        directory.coverages.set(validated_data['coverages'])
        directory.subjects.set(validated_data['subjects'])
        directory.keywords.set(validated_data['keywords'])
        directory.workareas.set(validated_data['workareas'])
        directory.languages.set(validated_data['languages'])
        directory.catalogers.set(validated_data['catalogers'])
        return directory

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.dir_layout = validated_data.get('dir_layout', instance.dir_layout)
        instance.banner_file = validated_data.get('banner_file', instance.banner_file)
        instance.parent = validated_data.get('parent', instance.parent)
        self.__create_update(instance)
        instance.individual_files.set(validated_data.get('individual_files', instance.individual_files.all()))
        instance.creators.set(validated_data.get('creators', instance.creators.all()))
        instance.coverages.set(validated_data.get('coverages', instance.coverages.all()))
        instance.subjects.set(validated_data.get('subjects', instance.subjects.all()))
        instance.keywords.set(validated_data.get('keywords', instance.keywords.all()))
        instance.workareas.set(validated_data.get('workareas', instance.workareas.all()))
        instance.languages.set(validated_data.get('languages', instance.languages.all()))
        instance.catalogers.set(validated_data.get('catalogers', instance.catalogers.all()))
        return instance

    def __create_update(self, directory):
        request = self.context['request']
        if 'banner_file' in request.FILES:
            directory.banner_file_uploaded = True
        directory.save()
        return directory

    class Meta:
        model = Directory
        fields = (
            'id', 'url', 'name', 'dir_layout', 'individual_files', 'banner_file', 'original_file_name',
            'creators', 'coverages', 'subjects', 'keywords', 'workareas', 'languages', 'catalogers', 'parent',
        )
        read_only_fields = ('original_file_name',)
        validators = [
            DirectoryNameUniqueValidator()
        ]
        extra_kwargs = {
            'url': {'lookup_field': 'pk'},
        }
