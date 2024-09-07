import sys

sys.path.append('/Users/lsy/person/workspace/n-s-framework')

from ai.translate.novel_translate import translate_novel_text_and_refine_with_error_handling, translate_title_and_refine_with_error_handling
from common.dao.mysql_common import fetch_data_and_convert_to_class, insert_objects_to_db
from common.model.novel_info_model import ChapterInfo, NovelInfo
from common.db.mysql import novel_connection
from common.model.novel_translate_model import ChapterTranslateInfo, NovelTranslateInfo

def translate_novel():
    start_id = 232
    novel_extra_condition = f'where id > {start_id} order by id'
    novel_list = fetch_data_and_convert_to_class(novel_connection, 'novel_info', NovelInfo, ignore_fields=['chapters'], extra_condition=novel_extra_condition)
    for novel in novel_list:
        novel_translates = []
        chapter_translates = []
        chapter_extra_condition = f'where novel_href = "{novel.href}" order by chapter_index'
        chapter_list = fetch_data_and_convert_to_class(novel_connection, 'chapter_info', ChapterInfo, extra_condition=chapter_extra_condition)
        novel_translate_info = NovelTranslateInfo()
        novel_title = translate_title_and_refine_with_error_handling(novel.title)
        novel_abstract = translate_novel_text_and_refine_with_error_handling(novel.abstract)
        novel_translate_info.base_id = novel.id
        novel_translate_info.title = novel_title
        novel_translate_info.abstract = novel_abstract
        novel_translates.append(novel_translate_info)
        for chapter in chapter_list:
            chapter_translate_info = ChapterTranslateInfo()
            chapter_title = translate_title_and_refine_with_error_handling(chapter.chapter_title)
            content_before = ''
            if chapter.content_before != '':
                content_before = translate_novel_text_and_refine_with_error_handling(chapter.content_before)
            content = translate_novel_text_and_refine_with_error_handling(chapter.content)
            content_after = ''
            if chapter.content_after != '':
                content_after = translate_novel_text_and_refine_with_error_handling(chapter.content_after)
            chapter_translate_info.base_id = chapter.id
            chapter_translate_info.chapter_title = chapter_title
            chapter_translate_info.content_before = content_before
            chapter_translate_info.content = content
            chapter_translate_info.content_after = content_after
            chapter_translates.append(chapter_translate_info)
        insert_objects_to_db(novel_connection, 'novel_translate_info', novel_translates, ignore_fields=['id'])
        insert_objects_to_db(novel_connection, 'chapter_translate_info', chapter_translates, ignore_fields=['id'])

def main():
    translate_novel()

if __name__=="__main__":
    main()