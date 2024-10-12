from django.test import TestCase
from media_platform.models import Content
from media_platform.models import Channel
from django.core.files import File
import shutil
import os


class ChannelTestCase(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        # Remove images stored in media while testing
        try:
            shutil.rmtree(
                os.path.join("media", "media_platform", "picture", "tests")
            )
        except FileNotFoundError:
            pass

    def test_channel_with_sub_channel_and_content(self):
        # TODO: No se como crear el canal con contenido ya existente
        # Check that channels cannot have both sub channels and content
        content = Content(rating=5)
        content.save()

        with open(os.path.join("media_platform", "tests", "media", "netflix.png"), "rb") as f:
            channel1 = Channel(
                title="Netflix",
                language=1,
                picture=File(f, name=os.path.join("tests", "netflix.png"))
            )
            channel1.save()
        channel1.content.add(content)

        with open(os.path.join("media_platform", "tests", "media", "netflix.png"), "rb") as f:
            channel2 = Channel(
                title="Channel with sub channel and content",
                language=1,
                picture=File(f, name=os.path.join("tests", "netflix.png"))
            )
            channel2.save()
        channel2.sub_channels.add(channel1)
        channel2.content.add(content)

        self.assertRaises(Exception, channel2.save)

