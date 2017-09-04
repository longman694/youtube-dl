# coding: utf-8
from __future__ import unicode_literals

import re
import json

from .common import InfoExtractor
from ..utils import (
    ExtractorError,
    js_to_json,
    write_string,
    RegexNotFoundError
)


class SeemeIE(InfoExtractor):
    IE_NAME = 'seeme.me'
    IE_DESC = 'MThai'
    _VALID_URL = r'https?://(?:www\.)?seeme\.me/ch/[^/]+/(?P<id>[^/?#&]+)'
    _TESTS = [
        {
            'url': 'https://seeme.me/ch/monofilm/M2WD8q?pl=9EqKYz',
            'info_dict': {
                'id': 'M2WD8q',
                'ext': 'm3u8',
                'title': 'แฮปปี้เบิร์ธเดย์ Happy Birthday (เต็มเรื่อง)',
                'thumbnail': r're:^https?://.*\.jpg$',
            },
            'params': {
                'skip_download': 'm3u8 download'
            }
        },
    ]

    def _real_extract(self, url):
        video_id = self._match_id(url)
        webpage = self._download_webpage(url, video_id, fatal=False)

        if not webpage:
            # Page sometimes returns captcha page with HTTP 403
            raise ExtractorError(
                'Unable to access page. You may have been blocked.',
                expected=True)

        mobj = re.search(r'\"sources\":\[(.*?)\],', webpage)
        if mobj is None:
            raise ExtractorError('Unable to extract video')

        d = json.loads(mobj.group(1))

        formats = self._extract_m3u8_formats(d['file'], video_id, 'mp4')
        self._sort_formats(formats)

        return {
            'id': video_id,
            'title': self._og_search_title(webpage),
            'description': self._og_search_description(webpage),
            'formats': formats,
        }

