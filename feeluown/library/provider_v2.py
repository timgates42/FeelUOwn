from typing import Optional

from feeluown.media import Media, Quality
from feeluown.models import ModelType
from .flags import Flags


def check_flags(provider, model_type: ModelType, flags: Flags):
    return provider.meta.flags.get(model_type, Flags.none) & flags


class ProviderV2:
    class meta:
        identifier: str = ''
        name: str = ''
        flags: dict = {}

    check_flags = check_flags

    def song_list_similar(self, song):
        """List similar songs

        flag: (ModelType.song, Flags.similar_song)
        """

    def song_list_quality(self, song):
        pass

    def song_get_media(self, song, quality):
        pass

    def song_select_media(self, song, policy) -> Optional[Media]:
        # fetch available quality list
        available_q_set = set(self.song_list_quality(song))
        if not available_q_set:
            return None

        QualityCls = Quality.Audio
        # translate policy into quality priority list
        if policy is None:
            policy = 'hq<>'
        sorted_q_list = Quality.SortPolicy.apply(
            policy, [each.value for each in list(QualityCls)])

        # find the first available quality
        for quality in sorted_q_list:
            if quality in available_q_set:
                break
        return self.song_get_media(song, quality), quality
