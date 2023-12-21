from rest_framework import serializers
from .models import Support
from rest_framework import generics


class SupportSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Support
        fields = "__all__"

# class SupportModel:
#     def __init__(self, title, content):
#         self.title = title
#         self.content = content


# class SupportSerializer(serializers.Serializer):
#     title = serializers.CharField(max_length=255)
#     slug=serializers.SlugField(max_length=255)
#     content = serializers.CharField()
#     photo=serializers.FileField()
#     time_create = serializers.DateTimeField(read_only=True)
#     time_update = serializers.DateTimeField(read_only=True)
#     is_published = serializers.BooleanField(default=True)
#     cat_id = serializers.IntegerField()
#
#
#
#     def create(self, validated_data):
#
#         return Support.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         instance.title = validated_data.get("title", instance.title)
#         instance.slug = validated_data.get("slug", instance.slug)
#         instance.content = validated_data.get("content", instance.content)
#         instance.time_update = validated_data.get("time_update", instance.time_update)
#         instance.is_published = validated_data.get("is_published", instance.is_published)
#         instance.cat_id = validated_data.get("cat_id", instance.cat_id)
#         instance.save()
#         return instance
#
#
#


# def encode():
#     model = SupportModel('Grants', 'Content: Expensive')
#     model_sr = SupportSerializer(model)
#     print(model_sr.data, type(model_sr.data), sep='\n')
#     json = JSONRenderer().render(model_sr.data)
#     print(json)
#
#
# def decode():
#     stream = io.BytesIO(b'{"title":"Grants","content":"Content: Expensive"}')
#     data = JSONParser().parse(stream)
#     serializer = SupportSerializer(data=data)
#     serializer.is_valid()
#     print(serializer.validated_data)
