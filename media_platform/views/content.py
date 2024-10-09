from media_platform.models import Content
from media_platform.serializers import ContentSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics


class ContentList(generics.ListAPIView):
    """
    Queryset that retrieves and filters channels of the highest level (no other channel uses this channel as subchannel)
    """
    # def get_queryset(self):
    #     # Filter all channels that have sub_channels
    #     subchannels = Channel.objects.exclude(sub_channels__isnull=True).all().values_list("sub_channels", flat=True)
    #     return Channel.objects.exclude(id__in=subchannels).all()
    queryset = Content.objects.all()
    serializer_class = ContentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['rating']
