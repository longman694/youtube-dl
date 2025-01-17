# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from time import time

from .common import InfoExtractor


class LineTVIE(InfoExtractor):
    IE_NAME = 'tv.line.me'
    IE_DESC = 'LINE TV Thailand'
    _GEO_COUNTRIES = ['TH']
    _VALID_URL = r'https?://tv\.line\.me/(v|embed)/(?P<id>\d+)(?:_.+)?(?:/list/\d+)?'
    _TESTS = [
        {
            'url': u'https://tv.line.me/v/1800305_club-friday-the-series-8-'
                   u'รักแท้มีหรือไม่มีจริง-ตอนรักแท้หรือแค่สับสน-ep4-5-5/list/135464',
            'md5': 'aff2e0e78037df9f780225129b81b66f',
            'info_dict': {
                'id': '1800305',
                'ext': 'mp4',
                'title': u'Club Friday The Series 8 รักแท้...มีหรือไม่มีจริง '
                         u'ตอนรักแท้หรือแค่...สับสน EP.4 [5/5]',
                'thumbnail': 'https://phinf.pstatic.net/tvcast/20170624_255/'
                             'dRCpL_14982404693141P37s_PNG/1498240469243.png?'
                             'type=f640',
            }
        }, {
            'url': u'https://tv.line.me/v/1903589/list/143699',
            'info_dict': {
                'id': '1903589',
                'ext': 'mp4',
                'title': u'วิธีทำ เมนู “บลูเบอร์รีครัมเบิลมัฟฟิน” ฟินจนเพื่อนต้องห่อกลับบ้าน',
            }
        }
    ]

    def _real_extract(self, url):
        video_id = self._match_id(url)
        print video_id
        print url

        webpage = self._download_webpage(url, video_id)

        meta = self._html_search_regex(r'var rmcplayer = new naver.WebPlayer\(([^)]*)\);', webpage, 'meta')
        print meta
        real_video_id = self._search_regex("videoId:\s*'([^']*)'", meta, 'video id')
        print real_video_id

        key = self._search_regex("key:\s*'([^']*)'", meta, 'key')
        print key

        service_id = self._search_regex("serviceId:\s*(\d+)", meta, 'service id')
        print service_id

        ts = int(round(time()*10000000))

        video_info_url = 'https://global-nvapis.line.me/linetv/rmcnmv/vod_play_videoInfo.json?key={0}&' \
                         'pid=rmcPlayer_{1}&sid={2}&ver=2.0&devt=html5_mo&doct=json&ptc=https&cpt=vtt&' \
                         'ctls=%7B%22visible%22%3A%7B%22fullscreen%22%3Atrue%2C%22logo%22%3Afalse%2C%22' \
                         'playbackRate%22%3Afalse%2C%22scrap%22%3Afalse%2C%22playCount%22%3Atrue%2C%22' \
                         'commentCount%22%3Atrue%2C%22title%22%3Atrue%2C%22writer%22%3Atrue%2C%22expand%22%3A' \
                         'true%2C%22subtitles%22%3Atrue%2C%22thumbnails%22%3Atrue%2C%22quality%22%3Atrue%2C%22' \
                         'setting%22%3Atrue%2C%22script%22%3Afalse%2C%22logoDimmed%22%3Atrue%2C%22badge%22%3Atrue%2C' \
                         '%22seekingTime%22%3Atrue%2C%22linkCount%22%3Afalse%2C%22createTime%22%3Afalse%2C%22' \
                         'thumbnail%22%3Atrue%7D%2C%22clicked%22%3A%7B%22expand%22%3Afalse%2C%22subtitles%22' \
                         '%3Atrue%7D%7D&lc=th_TH&adi=%5B%7B%22type%22%3A%22pre%22%2C%22exposure%22%3Atrue%2C%22' \
                         'replayExposure%22%3Atrue%2C%22interval%22%3Anull%2C%22timeTable%22%3Anull%7D%2C%7B%22' \
                         'type%22%3A%22post%22%2C%22exposure%22%3Afalse%2C%22replayExposure%22%3Afalse%2C%22' \
                         'interval%22%3Anull%2C%22timeTable%22%3Anull%7D%5D&' \
                         'adu=https%3A%2F%2Fad-cpv.line.me%2Ffxshow%3Fsu%3DSU10151%26cp%3D1549%26st%3D3671%26' \
                         'chl%3Dmakeitright2%26cat%3DDRAMA%26cl%3D1799583%26svc%3Dlinetv%26cc%3DN%26ctry%3DTH%26' \
                         'v_pid%3D31910%26dmg%3D&videoId={3}&cc=TH&sm=linetv'.format(key, ts, service_id, real_video_id)

        video_info = self._parse_json(self._download_webpage(video_info_url, video_id), video_id)

        formats = []

        for f in video_info['videos']['list']:
            ff = {'url': f['source'],
                  'width': f['encodingOption']['width'],
                  'height': f['encodingOption']['height'],
                  }
            formats.append(ff)

        return {
            'id': video_id,
            'title': video_info['meta']['subject'],
            'thumbnail': video_info['meta']['cover']['source'],
            'formats': formats,
        }

