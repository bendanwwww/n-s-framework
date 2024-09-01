from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
import scrapy

from common.model.novel_info_model import ChapterInfo, NovelInfo

ROUTE_URL = "https://ncode.syosetu.com/"
URL = "https://yomou.syosetu.com/search.php?&type=er&order_former=search&order=new&notnizi=1&p={page}"
NOVEL_MODEL_KEY = "novel"
CAPTER_MODEL_KEY = "capter"
CAPTER_TIME_FORMAT = "%Y/%m/%d %H:%M"

class Syosetu(scrapy.Spider):

    name = 'syosetu'
    start_urls = []
    for page in range(1, 2) :
        start_urls.append(URL.format(page=page))

    def __init__(self, *args, **kwargs):
        super(Syosetu, self).__init__(*args, **kwargs)
        self.executor = ThreadPoolExecutor(max_workers=5)
   
    def parse(self, response):
        novels = response.xpath('//div[@class="searchkekka_box"]')
        for novel in novels:
            novel_info = NovelInfo()
            novel_h = novel.xpath("./div")
            href = novel_h.xpath("./a/@href").extract()[0]
            title = novel_h.xpath("./a/text()").extract()[0]
            author = novel.xpath("./a/text()").extract()[0]
            n_code = novel.xpath("./text()").extract()[-2].split('：')[-1].replace('\n', '')
            novel_info.href = href
            novel_info.title = title
            novel_info.author = author
            novel_info.n_code = n_code
            yield scrapy.Request(novel_info.href, meta={NOVEL_MODEL_KEY: novel_info}, callback=self.novel_chapter_list)

    def novel_chapter_list(self, response):
        novel_info = response.meta[NOVEL_MODEL_KEY]
        chapters = response.xpath('//dl[@class="novel_sublist2"]')
        for i, chapter in enumerate(chapters):
            chapter_info = ChapterInfo()
            chapter_title = chapter.xpath('./dd/a/text()').extract()[0].replace('\n', '')
            chapter_href = chapter.xpath('./dd/a/@href').extract()[0].replace('\n', '')
            chapter_write_time = chapter.xpath('./dt/text()').extract()[0].replace('\n', '')
            chapter_info.novel_href = novel_info.href
            chapter_info.novel_title = novel_info.title
            chapter_info.novel_author = novel_info.author
            chapter_info.novel_n_code = novel_info.n_code
            chapter_info.chapter_index = i + 1
            chapter_info.chapter_title = chapter_title
            chapter_info.chapter_href = ROUTE_URL + chapter_href
            chapter_info.write_time = int(datetime.strptime(chapter_write_time, CAPTER_TIME_FORMAT).timestamp())
            yield scrapy.Request(chapter_info.chapter_href, meta={NOVEL_MODEL_KEY: novel_info, CAPTER_MODEL_KEY: chapter_info}, callback=self.novel_chapter_content)

    def novel_chapter_content(self, response):
        novel_info = response.meta[NOVEL_MODEL_KEY]
        chapter_info = response.meta[CAPTER_MODEL_KEY]
        chapter_contents = response.xpath('//div[@class="novel_view"]')
        for content in chapter_contents:
            texts = content.xpath('./p[*]')
            for text in texts:
                t = ''
                ts = text.xpath('./text()').extract()
                if len(ts) == 0:
                    t = '\n'
                else:
                    t = ts[0].replace('\n', '')
                chapter_info.content.append(t)
                novel_info.chapters.append(chapter_info)
        return novel_info
            