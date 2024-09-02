from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from common.tools.proxy_tool import proxy_https
import scrapy

from common.model.novel_info_model import ChapterInfo, NovelInfo, TagInfo

ROUTE_URL = "https://ncode.syosetu.com"
URL = "https://yomou.syosetu.com/search.php?&type=er&order_former=search&word={word}&order={order}&notnizi=1&p={page}"
PROXY_KEY = "proxy"
NOVEL_MODEL_KEY = "novel"
CAPTER_MODEL_KEY = "capter"
CAPTER_TIME_FORMAT = "%Y/%m/%d %H:%M"

class Syosetu(scrapy.Spider):

    # spider field
    name = 'syosetu'
    start_urls = []
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Cookie': '_unv_aid=2ac5017694ae41fcc26dfa9bde97eeca; __td_signed=true; _ga=GA1.1.946796567.1725169859; _im_vid=01J6P25ZVZ5SMB9D6K4AKXJMKV; _pubcid=9aafa188-cbb5-4448-9991-6d85e20e0492; _pubcid_cst=zix7LPQsHA%3D%3D; ks2=t4xexuda4vzw; sasieno=0; lineheight=0; fontsize=0; novellayout=1; fix_menu_bar=1; _im_vid=01J6P25ZVZ5SMB9D6K4AKXJMKV; _im_vid=01J6P25ZVZ5SMB9D6K4AKXJMKV; _flux_dataharbor=1; __pmguid_=a058e59d-a594-4035-b7aa-3764fe9f4e09; __mguid_=10f9287d669d343325qui800ly5jpqs7; adr_id=5WNBA2vv4t971ja3lj9MtlKclVoPXiXtqV2AlkgpZjsVWptA; nlist1=19eed.1-1d0t5.2; _yjsu_yjad=1725181715.5909c44c-ae67-4c59-aa23-8cd689e2b2df; _unv_id=01J6HVNGNS8SADJEC96RVJGS00; _ga_2YQV7PZTL9=GS1.1.1725257298.5.1.1725259322.0.0.0; cto_bundle=9d-e1l9RJTJGdXQlMkZ5RGdZTldqOWglMkZFaWpHYk5scFFpVVVKWWclMkJ2YnpjUmlPVjVjVE5xWGdPSXBza28lMkZ6Wm9lMVUlMkJpRTFJMHhwTTVRcjc3T09LV2ZBNGdDWiUyRkk4TnRmWWxhckVmNkwyRjVtZXdGUUd2c3FKRXJEc0pkNXRnNzVpSkplSXhZWTJQRkxWZlFNTEt0ak5zdzJDSUVFcVN1RGhBdDkxQXhONFI3U0RrTWQ5dDloTkdlU2dPMEV0MDkwS2ZwalFaNA; cto_bidid=YrKBt19PYUlUQTVCQmRpbyUyRjVNMThPU3JkNGk5d0pvTnQ5Tjl2T3VWYklYaHh4N2REZEE2aVYlMkZnYyUyQjNwVzdzZHVhajBtQnZRSEhLWDB6OERJWWc1aHhrZFRaa05QTHoySHpMTlNvWVdaaExYTTk2Qms3OEdjZzMzeW8lMkZPaUhEZ2RYWTZyWWZNekFpJTJGZENJZEMxS09WQWc2czVBJTNEJTNE; _ga_1TH9CF4FPC=GS1.1.1725254792.7.1.1725260417.0.0.0; __gads=ID=057fdd661442b3ea:T=1725170375:RT=1725260417:S=ALNI_MaNNnQFHGVsAdGfqXp2Ys7tbZadgw; __gpi=UID=00000ee44d280bfd:T=1725170375:RT=1725260417:S=ALNI_MbrTE7NFjPa0yQrFDHK2va-kStm0g; __eoi=ID=7771f53c73aa71c8:T=1725170375:RT=1725260417:S=AA-AfjaRk9BV_ngFXLoUSMkQHTj9; _td=06de911a-ca6a-4890-8e03-1c8b10bd8063',
        # 'Host': 'yomou.syosetu.com',
        # 'Referer': 'https://yomou.syosetu.com/',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        }
    custom_settings = {'DEFAULT_REQUEST_HEADERS': headers}

    # business field
    order = 'new'
    word = ''

    for page in range(1, 2) :
        start_urls.append(URL.format(page=page, order=order, word=word))

    def __init__(self, *args, **kwargs):
        super(Syosetu, self).__init__(*args, **kwargs)
        self.executor = ThreadPoolExecutor(max_workers=5)
        
    # def start_requests(self):
    #     for url in self.start_urls:
    #         yield scrapy.Request(url=url, callback=self.parse, meta={PROXY_KEY: proxy_https})
   
    def parse(self, response):
        novels = response.xpath('//div[@class="searchkekka_box"]')
        for novel in novels:
            novel_info = NovelInfo()
            # base info
            novel_h = novel.xpath("./div")
            href = novel_h.xpath("./a/@href").extract()[0]
            title = novel_h.xpath("./a/text()").extract()[0]
            author = novel.xpath("./a/text()").extract()[0]
            n_code = novel.xpath("./text()").extract()[-2].split('：')[-1].replace('\n', '')
            # set base info
            novel_info.href = href
            novel_info.title = title
            novel_info.author = author
            novel_info.n_code = n_code
            # detail
            novel_table = novel.xpath('./table/tr')
            novel_state = 0
            ns = ''.join(novel_table.xpath('./td[@class="left"]/text()').extract())
            if '完結済' not in ns:
                novel_state = 1
            novel_abstract = novel_table.xpath('./td[2]/div[@class="ex"]/text()').extract()[0].replace('\n', '')
            novel_type = novel_table.xpath('./td[2]/a[1]/text()').extract()[0]
            novel_type_href = novel_table.xpath('./td[2]/a[1]/@href').extract()[0]
            novel_short_type = ''
            nsts = novel_table.xpath('./td[2]/text()').extract()
            for nst in nsts:
                if '〔' in nst and '〕' in nst:
                    novel_short_type = nst.replace('\n', '').replace('〔', '').replace('〕', '')
            novel_tags = []
            nts = novel_table.xpath('./td[2]/a')
            if len(nts) > 1:
                novel_tags = nts[1:]
            tags = []
            for tag in novel_tags:
                tag_info = TagInfo()
                tag_info.tag_name = tag.xpath('./text()').extract()[0]
                tag_info.tag_href = ROUTE_URL + tag.xpath('./@href').extract()[0]
                tags.append(tag_info)
            novel_last_update_time = ''
            nluts = novel_table.xpath('./td[2]/text()').extract()
            for nlut in nluts:
                if '最終更新日：' in nlut:
                    novel_last_update_time = nlut.replace('最終更新日：', '').replace('\u3000', '').strip()
                    break
            novel_text_size_read_time = novel_table.xpath('./td[2]/span[1]/text()').extract()[0].replace('読了時間：', '').split('（')
            # set detail
            novel_info.type = novel_type
            novel_info.type_href = ROUTE_URL + novel_type_href
            novel_info.short_type = novel_short_type
            novel_info.tags = tags
            novel_info.state = novel_state
            novel_info.last_update_time = int(datetime.strptime(novel_last_update_time, CAPTER_TIME_FORMAT).timestamp())
            novel_info.read_time = novel_text_size_read_time[0]
            novel_info.text_size = int(novel_text_size_read_time[1].replace('文字）', '').replace(',', ''))
            novel_info.abstract = novel_abstract
            yield scrapy.Request(novel_info.href, meta={NOVEL_MODEL_KEY: novel_info}, callback=self.novel_chapter_list)

    def novel_chapter_list(self, response):
        novel_info = response.meta[NOVEL_MODEL_KEY]
        chapters = response.xpath('//dl[@class="novel_sublist2"]')
        novel_info.chapter_number = len(chapters)
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
            