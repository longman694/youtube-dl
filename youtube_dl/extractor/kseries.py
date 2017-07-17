# coding: utf-8
from __future__ import unicode_literals

from youtube_dl.utils import RegexNotFoundError
from .common import InfoExtractor
from .googledrive import GoogleDriveIE
from ..utils import (
    ExtractorError,
    js_to_json,
)


class KSeriesIE(InfoExtractor):
    IE_NAME = 'kseries.co'
    IE_DESC = 'K series Thailand'
    _VALID_URL = r'https?://(?:www\.)?kseries\.co/clip/(?P<id>\d+)/'
    _TESTS = [
        {
            'url': 'http://www.kseries.co/clip/108093/',
            'info_dict': {
                'id': '108093',
                'ext': 'mp4',
                'title': 'Duel ซับไทย HD Ep.1',
                'thumbnail': r're:^https?://.*\.jpg$',
            },
        },
        {
            'url': 'http://www.kseries.co/clip/13980/',
            'info_dict': {
                'id': '13980',
                'ext': 'mp4',
                'title': 'ซีรีย์ญี่ปุ่น Death Note 2015 Ep.1-1',
                'thumbnail': r're:^https?://.*\.jpg$',
            },
        },
        {
            'url': 'http://www.kseries.co/clip/147831/',
            'info_dict': {
                'id': '147831',
                'ext': 'mp4',
                'title': 'Three Kingdoms เปิดตำราสามก๊ก Ep.10 HD',
                'thumbnail': r're:^https?://.*\.jpg$',
            },
        }
    ]

    def _real_extract(self, url):
        video_id = self._match_id(url)
        # print video_id
        webpage = self._download_webpage(url, video_id, fatal=False)

        if not webpage:
            # Page sometimes returns captcha page with HTTP 403
            raise ExtractorError(
                'Unable to access page. You may have been blocked.',
                expected=True)

        for n in [0, 1, 2]:
            player = self._download_webpage('http://www.kseries.co/clip/play.php?'
                                            'id={}&n={}'.format(video_id, n), video_id)

            title = self._og_search_title(webpage)
            try:
                video_url = self._html_search_regex('src="(https://docs.google.com/file/d/\w+/preview)"', player, 'g_url')
            except RegexNotFoundError:
                continue
            break

        ie = GoogleDriveIE()
        ie.set_downloader(self._downloader)

        info = ie.extract(video_url)
        info.update({
            'id': video_id,
            'title': title,
            'thumbnail': self._og_search_thumbnail(webpage),
        })
        return info
