from django.core.management.base import BaseCommand, CommandError, CommandParser
from media_platform.models import Channel
from django.db.models import Avg
import pandas as pd
import numpy as np


class Command(BaseCommand):
    help = "Efficiently calculates rating for all channels"

    def add_arguments(self, parser: CommandParser):
        parser.add_argument("path", type=str)

    def handle(self, *args, **options):
        csv_path = options["path"]

        # Calculate rating for all channels with content and get channels with subchannels
        channels_ratings = Channel.objects.raw(
            "SELECT * "
            "FROM ( "
            "	SELECT mpc.id as id_subchannel, mpc.title as title_subchannel, avg(mpcont.rating) as rating_subchannel "
            "	FROM media_platform_channel as mpc "
            "	JOIN media_platform_channel_content as mpcc "
            "	ON mpc.id = mpcc.channel_id  "
            "	JOIN media_platform_content as mpcont  "
            "	ON mpcc.content_id = mpcont.id "
            "	GROUP BY mpc.id "
            ") as group_content_rating "
            "LEFT JOIN media_platform_channel_sub_channels as mpcsc "
            "ON group_content_rating.id_subchannel = mpcsc.to_channel_id "
            "LEFT JOIN media_platform_channel as mpc "
            "ON mpcsc.from_channel_id = mpc.id;"
        )

        # Create pandas dataframe with recovered data
        df = pd.DataFrame(
            [(i.title, i.title_subchannel, i.rating_subchannel) for i in channels_ratings], columns=("title", "title_subchannel", "rating_subchannel")
        )

        # Get the average for channels with subchannels
        average_channels_with_subchannels = df.groupby(["title"])["rating_subchannel"].mean()

        # Get the average for channels with content
        average_channels_with_content = df[["title_subchannel", "rating_subchannel"]].drop_duplicates()
        average_channels_with_content = average_channels_with_content.rename(columns={"title_subchannel": "title", "rating_subchannel": "average_rating"})

        # Create dataframe with final data
        df = pd.concat((
            pd.DataFrame(
                {
                    "title": average_channels_with_subchannels.index,
                    "average_rating": average_channels_with_subchannels.values
                }, columns=("title", "average_rating")
            ),
            average_channels_with_content
        ))

        # Sort data by average descending
        df = df.sort_values("average_rating", ascending=False)

        # Rename columns
        df = df.rename(columns={"title": "channel title", "average_rating": "average rating"})

        # Store result in selected path
        df.to_csv(csv_path, index=False)
