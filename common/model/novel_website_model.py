class Book:
    def __init__(self):
        self.id = 0
        self.work_direction = 0
        self.cat_id = 0
        self.cat_name = ''
        self.pic_url = ''
        self.book_name = ''
        self.author_id = 0
        self.author_name = ''
        self.book_desc = ''
        self.score = 0.0
        self.book_status = 0
        self.visit_count = 0
        self.word_count = 0
        self.comment_count = 0
        self.yesterday_buy = 0
        self.last_index_id = 0
        self.last_index_name = ''
        self.last_index_update_time = 0
        self.is_vip = 0
        self.status = 0
        self.update_time = 0
        self.create_time = 0
        self.crawl_source_id = 0
        self.crawl_book_id = ''
        self.crawl_last_time = 0
        self.crawl_is_stop = 0
        
class BookIndex:
    def __init__(self):
        self.id = 0
        self.book_id = 0
        self.index_num = 0
        self.index_name = ''
        self.word_count = 0
        self.is_vip = 0
        self.book_price = 0
        self.storage_type = ''
        self.create_time = 0
        self.update_time = 0

class BookContent:
    def __init__(self):
        self.id = 0
        self.index_id = 0
        self.content = 0