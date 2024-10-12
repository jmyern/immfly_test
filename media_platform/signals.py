from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from media_platform.models import Content
from media_platform.models import Channel


@receiver(pre_save, sender=Content)
def check_content_rating_values(sender, instance: Content, **_):
    if instance.rating < 0 or instance.rating > 10:
        raise Exception(f"Value {instance.rating} forbidden for Content")


@receiver(post_save, sender=Channel)
def check_channel_references(sender, instance: Channel, **_):
    # WARNING: Should add a check so that you cannot create circular subchannels. May result in infinite loops.

    # Check that channel has either sub_channels or content
    if instance.sub_channels.count() > 0 and instance.content.count() > 0:
        title = instance.title
        instance.delete()
        raise Exception(f"Channel {title} cannot have both sub_channels and content")
