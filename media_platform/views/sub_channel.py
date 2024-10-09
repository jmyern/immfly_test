from media_platform.models import Channel
from media_platform.serializers import ChannelSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics


class SubChannelList(generics.ListAPIView):
    """
    Queryset that retrieves and filters all sub_channels of a parent channel
    """
    def get_queryset(self):
        channel_id = self.kwargs["channel_id"]
        subchannels = Channel.objects.filter(id=channel_id).exclude(sub_channels__isnull=True).values_list("sub_channels", flat=True)

        return Channel.objects.filter(id__in=subchannels).all()

    serializer_class = ChannelSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'title', 'language']
