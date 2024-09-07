import sys
sys.path.append('/Users/lsy/person/workspace/n-s-framework')

from novel.syosetu.syosetu_spider import Syosetu
from scrapy.crawler import CrawlerProcess

def main():
    crawler_process = CrawlerProcess()
    crawler_process.crawl(Syosetu)
    crawler_process.start()

if __name__=="__main__":
    main()