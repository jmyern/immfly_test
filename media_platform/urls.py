from django.urls import path
from media_platform.views.channel import ChannelList
from media_platform.views.sub_channel import SubChannelList
from media_platform.views.content import ContentList


urlpatterns = [
    path('channel', ChannelList.as_view(), name="Channel List"),
    path('channel/<int:channel_id>/subchannels', SubChannelList.as_view(), name="Channel List"),
    path('channel/<int:channel_id>/content', ContentList.as_view(), name="Content List")
]
