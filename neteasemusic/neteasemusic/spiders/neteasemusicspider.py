# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
import scrapy
from music.models import *
import datetime
from neteasemusic.utils.util import get_music_url
class NeteaseMusicSpider(scrapy.Spider):
    name = 'music'
    start_urls = 'http://music.163.com/discover/artist/'
    allowed_domains = ["music.163.com"]
    domain = 'http://music.163.com'
    singer_count = 0


    def start_requests(self):
        print u'==================开始爬歌曲================='
        yield scrapy.Request(url=self.start_urls, method='GET', callback=self.parse)

    def parse(self, response):
        body = response.body
        type_list = Selector(text=body).xpath("//a[@class='cat-flag']").extract()
        for t in type_list:
            if u'华语' in t:
                sub_type = Selector(text=t).xpath("//a/text()").extract_first()
                type_href = Selector(text=t).xpath("//a/@href").extract_first()
                id = int(type_href[type_href.rindex('=')+1:])
                if not MusicLanguage.objects.filter(id=id).exists():
                    MusicLanguage.objects.create(id=id, name=sub_type)
                sub_url = '/'.join([self.domain, type_href])
                print u'正在爬取[{}]歌曲, url:{} ...'.format(sub_type, type_href)
                yield scrapy.Request(url=sub_url,
                                     method="GET",
                                     callback=self.spell_parse, meta={"language": id})

    def spell_parse(self, response):
        body = response.body
        href_list = Selector(text=body).xpath("//ul[@id='initial-selector']//a/@href").extract()
        for href in href_list:
            if int(href[href.rindex('=') + 1:]) >= 0:
                sub_url = '/'.join([self.domain, href])
                yield scrapy.Request(url=sub_url,
                                     method="GET",
                                     callback=self.name_parse, meta={"language": response.meta['language']})

    def name_parse(self, response):
        body = response.body
        tag_a_list = Selector(text=body).xpath("//a[@class='nm nm-icn f-thide s-fc0']").extract()
        for tag in tag_a_list:
            self.singer_count += 1
            singer_name = Selector(text=tag).xpath("//a/text()").extract_first()
            singer_href = Selector(text=tag).xpath("//a/@href").extract_first()
            mark_index = singer_href.rindex('?')
            singer_href = singer_href[:mark_index] + '/album' + singer_href[mark_index:]
            sub_url = '/'.join([self.domain, singer_href])
            print u'正在爬取第[{}]个歌手[{}]的歌曲, url:{} ...'.format(self.singer_count, singer_name, singer_href)
            yield scrapy.Request(url=sub_url,
                                 method="GET",
                                 callback=self.singer_parse, 
                                 meta={"language": response.meta['language']})

    def singer_parse(self, response):
        body = response.body
        #h2 = Selector(text=body).xpath("//div[@class='n-artist f-cb']/div[@class='btm']/h2").extract_first()
        #print '>>>>>>>>>>>>>>{}'.format(h2)
        http404 = Selector(text=body).xpath("//div[@class='n-for404']").extract_first()
        if http404:
            print u'url: {} ...404'.format(response.url)
            return
        singer_name = Selector(text=body).xpath("//h2[@id='artist-name']/text()").extract_first()
        singer_id = Selector(text=body).xpath("//h2[@id='artist-name']/@data-rid").extract_first()
        singer_img = Selector(text=body).xpath("//div[@class='n-artist f-cb']/img/@src").extract_first()
        if not Singer.objects.filter(id=singer_id).exists():
            Singer.objects.create(id=singer_id, 
                                name=singer_name, 
                                image=singer_img,
                                language_id=response.meta['language'])

        tag_li_list = Selector(text=body).xpath("//ul[@id='m-song-module']/li").extract()
        for tag in tag_li_list:
            album_name = Selector(text=tag).xpath("//a[@class='tit s-fc0']/text()").extract_first()
            album_id = Selector(text=tag).xpath("//a[@class='icon-play f-alpha']/@data-res-id").extract_first()
            album_img = Selector(text=tag).xpath("//img/@src").extract_first()
            album_time = datetime.datetime.strptime(Selector(text=tag).xpath("//span[@class='s-fc3']/text()").extract_first(), "%Y.%m.%d").date()
            album_href = Selector(text=tag).xpath("//a[@class='tit s-fc0']/@href").extract_first()
            print u'正在爬取第[{}]个歌手[{}]的专辑<<{}>>, url:{} ...'.format(self.singer_count, singer_name, album_name, album_href)
            if not Album.objects.filter(id=album_id).exists():
                Album.objects.create(id=album_id, 
                                name=album_name, 
                                image=album_img,
                                time=album_time,
                                singer_id=singer_id)
            sub_url = '/'.join([self.domain, album_href])   
            yield scrapy.Request(url=sub_url,
                                 method="GET",
                                 callback=self.music_parse, 
                                 meta={"album_id": album_id, "singer_id": singer_id})

    def music_parse(self, response):
        body = response.body
        tr_list = Selector(text=body).xpath("//table[@class='m-table']/tbody/tr").extract()
        for tr in tr_list:
            music_href = Selector(text=tr).xpath("//tr/td/div[@class='f-cb']/div/div/span/a/@href").extract_first()
            music_id = int(music_href[music_href.rindex('=')+1:])
            music_url = get_music_url(music_id)
            if music_url:
                music_name = Selector(text=tr).xpath("//tr/td/div[@class='f-cb']/div/div/span/a/b/@title").extract_first()
                music_duration = Selector(text=tr).xpath("//tr/td[@class='s-fc3']/span[@class='u-dur']/text()").extract_first()
                print u'正在爬取歌曲<<{}>>, url:{} ...'.format(music_name, music_url)
                if not Music.objects.filter(id=music_id).exists():
                    Music.objects.create(id=music_id, 
                                    name=music_name, 
                                    url=music_url,
                                    duration=music_duration,
                                    singer_id=response.meta['singer_id'],
                                    album_id=response.meta['album_id'])

   