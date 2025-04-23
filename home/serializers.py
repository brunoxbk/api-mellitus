from rest_framework import serializers
from .models import Category, PostPage
from wagtail.images.models import Image
import base64 as b64
from django.conf import settings
from wagtail.admin.rich_text.converters.editor_html import EditorHTMLConverter
import os


def image_to_base64(image_path):
    with open(image_path, "rb") as img_file:
        encoded_string = b64.b64encode(img_file.read())
        return encoded_string.decode('utf-8')


# image_path = 'caminho_para_sua_imagem'
# base64_string = image_to_base64(image_path)
# print(base64_string)



class ImageSerializer(serializers.ModelSerializer):

    base64 = serializers.SerializerMethodField()

    def get_base64(self, obj):
        return image_to_base64(settings.PROJECT_DIR + obj.file.url)

    class Meta:
        model = Image
        fields = [
            "id",
            "title",
            "file",
            "base64"
        ]


class ImageEmbSerializer(serializers.ModelSerializer):
    file = serializers.SerializerMethodField()

    def get_file(self, obj):
        return obj.get_rendition("original").url

    class Meta:
        model = Image
        fields = [
            "id",
            "title",
            "file"
        ]


class CategorySerializer(serializers.ModelSerializer):
    image = ImageSerializer()
    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "slug",
            "image"
        ]


class CategoryEmbSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "slug"
        ]


class PostPageSerializer(serializers.ModelSerializer):
    cover = ImageEmbSerializer()
    categories = CategoryEmbSerializer(many=True)

    body = serializers.SerializerMethodField()

    def get_body(self, obj):
        html = EditorHTMLConverter().from_database_format(obj.body)
        return html.replace('src="/media/', 'src="' + settings.WAGTAILADMIN_BASE_URL + '/media/')
    
    class Meta:
        model = PostPage
        fields = [
            "id",
            "title",
            "subtitle",
            "body",
            "categories",
            "url_video",
            "has_video",
            "owner",
            "cover"
        ]



# -------------------

class RecursiveField(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data

class PostPageSerializer2(serializers.ModelSerializer):
    cover_url = serializers.SerializerMethodField()
    cover = ImageEmbSerializer()
    categories = CategoryEmbSerializer(many=True)

    body = serializers.SerializerMethodField()

    def get_body(self, obj):
        html = EditorHTMLConverter().from_database_format(obj.body)
        return html.replace('src="/media/', 'src="' + settings.WAGTAILADMIN_BASE_URL + '/media/')
    
    class Meta:
        model = PostPage
        fields = [
            'id',
            'title',
            'subtitle',
            'url',
            'body',
            'cover',
            'cover_url',
            "url_video",
            "has_video",
            'categories']
    
    def get_cover_url(self, obj):
        if obj.cover:
            return obj.cover.get_rendition('original').url
        return None

class PageSerializer(serializers.ModelSerializer):
    children = RecursiveField(many=True, source='get_children')
    specific = serializers.SerializerMethodField()
    
    class Meta:
        model = PostPage
        fields = ['id', 'title', 'url', 'children', 'specific']
    
    def get_specific(self, obj):
        specific_obj = obj.specific
        if isinstance(specific_obj, PostPage):
            return PostPageSerializer(specific_obj).data
        return None