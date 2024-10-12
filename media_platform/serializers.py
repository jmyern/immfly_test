from rest_framework import serializers
from media_platform.models import Channel, Content


class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = ["id", "title", "language", "picture", "sub_channels", "content", "groups"]


class ContentSerializer(serializers.ModelSerializer):
    metadata = serializers.StringRelatedField(many=True)
    files = serializers.StringRelatedField(many=True)

    class Meta:
        model = Content
        fields = ["rating", "metadata", "files"]
