from django.test import TestCase
from media_platform.models import Content
from media_platform.models import Channel
from django.core.files import File
import shutil
import os


class ChannelTestCase(TestCase):
    def setUp(self):
        pass
        # self.channel1 = Channel(
        #     title="Netflix",
        #     language="English",
        #     picture=File(
        #         open(os.path.join("media_platform", "tests", "media", "netflix.png")),
        #         name=os.path.join("tests", "netflix.png")
        #     )
        # )
        # self.channel1.content.add
        # self.channel2 = Channel(
        #     title="Videos On Demmand",
        #     language="English",
        #     picture=File(
        #         open(os.path.join("media_platform", "tests", "media", "netflix.png")),
        #         name=os.path.join("tests", "netflix.png")
        #     )
        # )

    def tearDown(self):
        # Remove images stored in media while testing
        try:
            shutil.rmtree(
                os.path.join("media", "media_platform", "picture", "tests")
            )
        except FileNotFoundError:
            pass


    # def test_channel_without_references(self):
    #     # Check that channels cannot exist without sub channels or content
    #     self.assertRaises(Exception, Channel(
    #         title="Channel without content",
    #         language="English",
    #         picture=File(
    #             open(os.path.join("media_platform", "tests", "media", "netflix.png")),
    #             name=os.path.join("tests", "netflix.png")
    #         )
    #     ).save)


    def test_channel_with_sub_channel_and_content(self):
        # TODO: No se como crear el canal con contenido ya existente
        # Check that channels cannot have both sub channels and content
        content = Content(rating=5)
        content.save()

        with open(os.path.join("media_platform", "tests", "media", "netflix.png"), "rb") as f:
            channel1 = Channel(
                title="Netflix",
                language="English",
                picture=File(f, name=os.path.join("tests", "netflix.png"))
            )
            channel1.save()
        channel1.content.add(content)

        with open(os.path.join("media_platform", "tests", "media", "netflix.png"), "rb") as f:
            channel2 = Channel(
                title="Channel with sub channel and content",
                language="English",
                picture=File(f, name=os.path.join("tests", "netflix.png"))
            )
            channel2.save()
        channel2.sub_channels.add(channel1)
        channel2.content.add(content)

        self.assertRaises(Exception, channel2.save)

