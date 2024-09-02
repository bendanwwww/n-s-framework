class NovelInfo:
    def __init__(self): 
        self.href = ''
        self.title = ''
        self.author = ''
        self.n_code = ''
        # novel type
        self.type = ''
        self.type_href = ''
        # novel short type
        self.short_type = ''
        # novel tags
        self.tags = []
        # 0: finished 1: unfinished
        self.state = 0
        self.last_update_time = 0
        # how long does it take to finish reading
        self.read_time = ''
        self.text_size = 0
        self.chapter_number = ''
        self.abstract = ''
        self.chapters = []

class TagInfo:
    def __init__(self): 
        self.tag_name = ''
        self.tag_href = ''

class ChapterInfo:
    def __init__(self): 
        self.novel_href = ''
        self.novel_title = ''
        self.novel_author = ''
        self.novel_n_code = ''
        self.chapter_index = ''
        self.chapter_title = ''
        self.chapter_href = ''
        self.write_time = 0
        self.content = []

print(NovelInfo().__dict__)