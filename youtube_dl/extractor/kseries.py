# coding: utf-8
from __future__ import unicode_literals

import re

from .common import InfoExtractor
from .googledrive import GoogleDriveIE
from ..utils import (
    ExtractorError,
    js_to_json,
    RegexNotFoundError
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
                'description': r're:.*',
            },
        },
        {
            'url': 'http://www.kseries.co/clip/13980/',
            'info_dict': {
                'id': '13980',
                'ext': 'mp4',
                'title': 'ซีรีย์ญี่ปุ่น Death Note 2015 Ep.1-1',
                'thumbnail': r're:^https?://.*\.jpg$',
                'description': r're:.*',
            },
        },
        {
            'url': 'http://www.kseries.co/clip/147831/',
            'info_dict': {
                'id': '147831',
                'ext': 'mp4',
                'title': 'Three Kingdoms เปิดตำราสามก๊ก Ep.10 HD',
                'thumbnail': r're:^https?://.*\.jpg$',
                'description': r're:.*',
            },
        },
        {
            'url': 'http://www.kseries.co/clip/108043/',
            'info_dict': {
                'id': '108043',
                'ext': 'mp4',
                'title': 'Hero Zhao Zi Long จูล่ง ขุนพลเทพสงคราม พากย์ไทย Ep.1 HD',
                'thumbnail': r're:^https?://.*\.jpg$',
                'description': r're:.*',
            },
        },
        {
            'url': 'http://www.kseries.co/clip/975506/',
            'info_dict': {
                'id': '975506',
                'ext': 'mp4',
                'title': 'Wonderful Mama ซับไทย Ep.1',
                'thumbnail': r're:^https?://.*\.jpg$',
                'description': r're:.*',
            }
        }
    ]

    def _get_google_info(self, player):
        video_url = self._html_search_regex('src="(https://docs.google.com/file/d/\w+/preview)"', player, 'g_url')
        ie = GoogleDriveIE()
        ie.set_downloader(self._downloader)
        return ie.extract(video_url)

    def _get_jwplayer_info(self, player, video_id):
        params = self._parse_json(self._html_search_regex(
            r'(?s)jwplayer\("clipplayer"\).setup\((\{.*?\})\);',
            player, 'clipplayer'), video_id, transform_source=js_to_json)
        video_url = params['file']
        return {
            'id': video_id,
            'formats': [{
                'url': video_url,
                'ext': 'mp4',
            }],
        }

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

            try:
                info = self._get_google_info(player)

            except RegexNotFoundError:
                try:
                    info = self._get_jwplayer_info(player, video_id)
                    if re.findall(r'https?://www.kseries.co/clip/Loading', info['formats'][0]['url']):
                        continue
                except KeyError:
                    continue
                except ExtractorError:
                    continue
            break

        info.update({
            'id': video_id,
            'title': self._og_search_title(webpage),
            'thumbnail': self._og_search_thumbnail(webpage),
            'description': self._og_search_description(webpage),
        })

        return info
