from django.core.management.base import BaseCommand, CommandError
from media_platform.models import Channel
from django.db.models import Avg
import pandas as pd
import numpy as np


class Command(BaseCommand):
    help = "Efficiently calculates rating for all channels"

    def add_arguments(self, parser):
        parser.add_argument("path", type=str)

    def handle(self, *args, **options):
        csv_path = options["path"]

        # Calculate rating of channels with content
        channels_with_content = Channel.objects.filter(sub_channels__isnull=True).annotate(average_rating=Avg('content__rating'))

        # Calculate ratings of channels with sub channels
        channels_with_subchannels = Channel.objects.raw(
            "SELECT mpc_parent.id as id, avg(mpcont.rating) as average_rating, mpc_parent.title as title "
            "FROM media_platform_channel as mpc_parent "
            "JOIN media_platform_channel_sub_channels as mpcsc "
            "ON mpc_parent.id = mpcsc.from_channel_id "
            "JOIN media_platform_channel as sub_mpc "
            "ON mpcsc.to_channel_id = sub_mpc.id "
            "JOIN media_platform_channel_content as mpcc "
            "ON sub_mpc.id = mpcc.channel_id "
            "JOIN media_platform_content as mpcont "
            "ON mpcc.content_id = mpcont.id "
            "GROUP BY mpc_parent.id;"
        )

        # Get list of all channels
        channels = Channel.objects.all()

        # Join all information into a pandas dataframe
        # Assumes all titles for channels are unique
        df = pd.concat((
            pd.DataFrame(
                [(i.title, i.average_rating) for i in channels_with_subchannels], columns=("title", "average_rating")
            ),
            pd.DataFrame(
                [(i.title, i.average_rating) for i in channels_with_content], columns=("title", "average_rating")
            ))
        )

        # Combine channels without rating
        df.merge(
            pd.DataFrame(
                list(
                    channels.values("title")
                )
            ), on="title"
        )

        # Sort values by average_rating
        df = df.sort_values("average_rating", ascending=False)

        # Store in requested path
        df.to_csv(csv_path, index=False)
