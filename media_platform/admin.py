from django.contrib import admin
from media_platform.models import Channel, Content, ContentMetadata, ContentFile, Group


@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    fields = ("title", "language", "picture", "sub_channels", "content", "groups")


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    fields = ("rating",)


@admin.register(ContentMetadata)
class ContentMetadataAdmin(admin.ModelAdmin):
    fields = ("content", "key", "value")


@admin.register(ContentFile)
class ContentFileAdmin(admin.ModelAdmin):
    fields = ("content", "media_file")

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    fields = ("name",)
