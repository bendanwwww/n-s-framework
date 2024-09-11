import sys
sys.path.append('/Users/lsy/person/workspace/n-s-framework')

import datetime
from common.dao.mysql_common import fetch_data_and_convert_to_class, insert_objects_to_db
from common.db.mysql import novel_connection, novel_website_connection
from common.model.novel_info_model import NovelInfo, ChapterInfo
from common.model.novel_translate_model import NovelTranslateInfo, ChapterTranslateInfo
from common.model.novel_website_model import Book, BookContent, BookIndex

def convert():
    # novel
    novel_list = fetch_data_and_convert_to_class(novel_connection, 'novel_info', NovelInfo, ignore_fields=['chapters'])
    novel_translate_list = fetch_data_and_convert_to_class(novel_connection, 'novel_translate_info', NovelTranslateInfo)
    # chapter
    chapter_list = fetch_data_and_convert_to_class(novel_connection, 'chapter_info', ChapterInfo)
    chapter_translate_list = fetch_data_and_convert_to_class(novel_connection, 'chapter_translate_info', ChapterTranslateInfo)
    # novel and chapter dict
    novel_translate_dict = {}
    chapter_dict = {}
    chapter_translate_dict = {}
    for novel_translate in novel_translate_list:
        novel_translate_dict[novel_translate.base_id] = novel_translate
    for chapter in chapter_list:
        if chapter.novel_href not in chapter_dict:
            chapter_dict[chapter.novel_href] = []
        chapter_dict[chapter.novel_href].append(chapter)
    for chapter_translate in chapter_translate_list:
        chapter_translate_dict[chapter_translate.base_id] = chapter_translate
    # convert
    novel_website_list = []
    chapter_website_list = []
    chapter_content_website_list = []
    novel_id = 1
    chapter_id = 1
    for novel in novel_list:
        if novel.id not in novel_translate_dict:
            continue
        novel_translate = novel_translate_dict[novel.id]
        if novel.href not in chapter_dict:
            continue
        chapter_list = chapter_dict[novel.href]
        chapter_list = sorted(chapter_list, key=lambda chapterInfo:chapterInfo.chapter_index)
        # novel
        book = Book()
        book.id = novel_id
        book.work_direction = 0
        book.cat_id = -1
        book.cat_name = novel.type
        book.pic_url = ''
        book.book_name = novel_translate.title
        book.author_id = 0
        book.author_name = novel.author
        book.book_desc = novel_translate.abstract
        book.score = 0.0
        book.book_status = 1
        book.visit_count = 0
        book.word_count = novel.text_size
        book.comment_count = 0
        book.yesterday_buy = 0
        book.last_index_update_time = datetime.datetime.fromtimestamp(novel.last_update_time)
        book.is_vip = 0
        book.status = 1
        book.update_time = datetime.datetime.fromtimestamp(novel.last_update_time)
        book.create_time = datetime.datetime.fromtimestamp(novel.last_update_time)
        book.crawl_source_id = 0
        book.crawl_book_id = novel.id
        book.crawl_last_time = datetime.datetime.fromtimestamp(novel.last_update_time)
        book.crawl_is_stop = 1
        # chapter
        for chapter in chapter_list:
            chapter_translate = chapter_translate_dict[chapter.id]
            book_index = BookIndex()
            book_index.id = chapter_id
            book_index.book_id = novel_id
            book_index.index_num = chapter.chapter_index
            book_index.index_name = chapter_translate.chapter_title
            book_index.word_count = len(chapter_translate.content)
            book_index.is_vip = 0
            book_index.book_price = 0
            book_index.storage_type = 'db'
            book_index.create_time = datetime.datetime.fromtimestamp(novel.last_update_time)
            book_index.update_time = datetime.datetime.fromtimestamp(novel.last_update_time)
            chapter_website_list.append(book_index)
            book_content = BookContent()
            book_content.index_id = chapter_id
            book_content.content = chapter_translate.content.replace('\n', '<br />')
            chapter_content_website_list.append(book_content)
            # update book's last chapter
            book.last_index_id = chapter_id
            book.last_index_name = chapter_translate.chapter_title
            chapter_id += 1
        novel_website_list.append(book)
        novel_id += 1
    insert_objects_to_db(novel_website_connection, 'book', novel_website_list)
    insert_objects_to_db(novel_website_connection, 'book_index', chapter_website_list)
    insert_objects_to_db(novel_website_connection, 'book_content', chapter_content_website_list)

def main():
    convert()

if __name__=="__main__":
    main()
