# -*- coding: utf-8 -*-
import scrapy
from ..settings import HYPEM_HANDLE, MAX_PAGES


# $ scrapy crawl hypem
class HypemSpider(scrapy.Spider):
    name = 'hypem'
    start_urls = ['https://hypem.com/%s/%s/' % (HYPEM_HANDLE, page) for page in range(1, MAX_PAGES+1)]

    def parse(self, response):
        pageInfo = response.css('.haarp-section-track')

        for song in pageInfo:
            artist = song.css('.artist::text').get()
            title = song.css('.track::attr(title)').get() or song.css('.track_name::text').getall()[-1].strip()
            favCount = song.css('.haarp-fav-count::text').get()
            dateLoved = song.css('.track-info::text').getall()
            dateLoved = dateLoved[1] if 'Found via' in dateLoved[0] else dateLoved[0]
            hypemlink = song.css('.track::attr(href)').get()
            shortlink = song.css('.download > a::attr(href)').get() or song.css('.download-extra > a::attr(href)').get()

            songInfo = {
                'artist': artist, 
                'title': title,
                'favCount': favCount,
                'dateLoved': dateLoved,
                'url': response.urljoin(hypemlink) if hypemlink is not None else None,
            }
            
            if shortlink is None:
                yield songInfo
            else:
                yield response.follow(shortlink, callback=self.extractTrueUrls, headers=None, meta={'songInfo': songInfo, 'handle_httpstatus_all': True})

    def extractTrueUrls(self, response):
        songInfo = response.meta['songInfo']
        songInfo['source'] = response.url

        yield songInfo
