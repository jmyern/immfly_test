from media_platform.models import Content
from media_platform.models import Channel
from media_platform.serializers import ContentSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from django.db.models import QuerySet


class ContentList(generics.ListAPIView):
    """
    Queryset that retrieves and filters channels of the highest level (no other channel uses this channel as subchannel)
    """
    def get_queryset(self) -> QuerySet:
        # Filter all content for given channel
        channel_id = self.kwargs["channel_id"]
        channel = Channel.objects.filter(id=channel_id)[0]

        return channel.content.all()

    serializer_class = ContentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'rating']
