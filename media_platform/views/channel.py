from media_platform.models import Channel
from media_platform.serializers import ChannelSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from django.db.models import QuerySet


class ChannelList(generics.ListAPIView):
    """
    Queryset that retrieves and filters channels of the highest level (no other channel uses this channel as subchannel)
    """

    def get_queryset(self) -> QuerySet:
        # Filter all channels that have sub_channels
        subchannels = Channel.objects.exclude(sub_channels__isnull=True).all().values_list("sub_channels", flat=True)
        return Channel.objects.exclude(id__in=subchannels).all()

    serializer_class = ChannelSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'title', 'language', "sub_channels", "content", 'groups']

    def filter_queryset(self, queryset: QuerySet) -> QuerySet:
        for key, value in self.request.query_params.items():
            if key in ["format"]:
                continue

            if key != "groups":
                if value not in [None, ""]:
                    queryset = queryset.filter(**{key: value})

            else:
                # special case for groups
                if value not in [None, ""]:
                    # Get all channels for group
                    group_channels = Channel.objects.filter(groups__id=value).all()

                    # Iterate over given channels to find all parent channels
                    filter_channel_id = {i.id for i in group_channels}
                    check_ids = {i.id for i in group_channels}
                    check_channels = group_channels
                    while len(check_channels) > 0:
                        check_channels = Channel.objects.filter(sub_channels__id__in=check_ids).all()
                        check_ids = {i.id for i in check_channels}
                        filter_channel_id = filter_channel_id.union(check_ids)

                    # Filter queryset on found parent channels
                    queryset = queryset.filter(id__in=filter_channel_id)

        return queryset
