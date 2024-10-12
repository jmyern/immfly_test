from django.test import TestCase
from django.core.management import call_command
from media_platform.models import Content, Channel
from django.core.files import File
import pandas as pd
import os


class ContentTestCase(TestCase):
    def setUp(self):
        with open(os.path.join("media_platform", "tests", "media", "netflix.png"), "rb") as f:
            channel_with_content_1 = Channel(
                title="channel with content",
                language=1,
                picture=File(f, name=os.path.join("tests", "netflix.png"))
            )
            channel_with_content_1.save()
            for i in (1, 3, 5, 7, 9):
                c = Content(rating=i)
                c.save()
                channel_with_content_1.content.add(c)

            channel_with_content_2 = Channel(
                title="second channel with content",
                language=1,
                picture=File(f, name=os.path.join("tests", "netflix.png"))
            )
            channel_with_content_2.save()
            for i in (2, 7):
                c = Content(rating=i)
                c.save()
                channel_with_content_2.content.add(c)

            channel_with_subchannels_1 = Channel(
                title="channel with subchannels",
                language=1,
                picture=File(f, name=os.path.join("tests", "netflix.png"))
            )
            channel_with_subchannels_1.save()
            channel_with_subchannels_1.sub_channels.add(channel_with_content_1)

            channel_with_subchannels_2 = Channel(
                title="second channel with subchannels",
                language=1,
                picture=File(f, name=os.path.join("tests", "netflix.png"))
            )
            channel_with_subchannels_2.save()
            channel_with_subchannels_2.sub_channels.add(channel_with_content_1, channel_with_content_2)

            channel_with_subchannels_3 = Channel(
                title="channel with subchannels without rating",
                language=1,
                picture=File(f, name=os.path.join("tests", "netflix.png"))
            )
            channel_with_subchannels_3.save()
            channel_with_subchannels_3.sub_channels.add(
                channel_with_content_1,
                channel_with_content_2,
                channel_with_subchannels_1,
                channel_with_subchannels_2
            )

        self.csv_path = os.path.join("media_platform", "tests", "tmp_ratings_file.csv")
        args = [self.csv_path]
        call_command("calculate_ratings", *args, **{})

        self.df = pd.read_csv(self.csv_path)

    def tearDown(self):
        try:
            os.remove(self.csv_path)
        except FileNotFoundError:
            pass

    def test_channel_with_content(self):
        self.assertEqual(self.df.loc[self.df['title'] == "channel with content"]["average_rating"].iloc[0], 5)
        self.assertEqual(self.df.loc[self.df['title'] == "second channel with content"]["average_rating"].iloc[0], 4.5)

    def test_channel_with_subchannels(self):
        self.assertEqual(self.df.loc[self.df['title'] == "channel with subchannels"]["average_rating"].iloc[0], 5)
        self.assertEqual(self.df.loc[self.df['title'] == "second channel with subchannels"]["average_rating"].iloc[0], 4.75)

    def test_channel_with_subchannels_without_rating(self):
        self.assertEqual(self.df.loc[self.df['title'] == "channel with subchannels without rating"]["average_rating"].iloc[0], 4.75)

    def test_order(self):
        self.assertTrue(self.df["average_rating"].is_monotonic_decreasing)
