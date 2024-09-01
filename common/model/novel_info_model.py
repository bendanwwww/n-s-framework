class NovelInfo:
    def __init__(self): 
        self.href = ''
        self.title = ''
        self.author = ''
        self.n_code = ''
        self.type = ''
        self.tags = []
        self.last_update_time = 0
        self.read_time = ''
        self.text_size = ''
        self.chapter = ''
        self.abstract = ''
        self.chapters = []

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