class Base_Library:
    def __init__(self):
        self.author = None
        self.title = None
        self.year = None
        self.article = None
        self.link = None
        self.doi = None
        self.clear_author = None
        self.clear_title = None


class Scopus_Library(Base_Library):
    def __init__(self):
        Base_Library.__init__(self)
        self.id_author = None
        self.source_name = None
        self.volume = None
        self.issue = None
        self.start_page = None
        self.end_page = None
        self.number_of_pages = None
        self.citation = None
        self.source = "Scopus"

    def Print(self):
        return (
            str(self.author)
            + ", "
            + str(self.id_author)
            + ", "
            + str(self.title)
            + ", "
            + str(self.year)
            + ", "
            + str(self.source_name)
            + ", "
            + str(self.volume)
            + ", "
            + str(self.issue)
            + ", "
            + str(self.article)
            + ", "
            + str(self.start_page)
            + ", "
            + str(self.end_page)
            + ", "
            + str(self.number_of_pages)
            + ", "
            + str(self.citation)
            + ", "
            + str(self.doi)
            + ", "
            + str(self.link)
            + ", "
            + str(self.source)
        )


class WOS_Library(Base_Library):
    def __init__(self):
        Base_Library.__init__(self)
        self.volume = None
        self.issue = None
        self.start_page = None
        self.end_page = None
        self.number_of_pages = None
        self.source = "WOS"

    def Print(self):
        return (
            str(self.author)
            + ", "
            + str(self.title)
            + ", "
            + str(self.year)
            + ", "
            + str(self.volume)
            + ", "
            + str(self.issue)
            + ", "
            + str(self.article)
            + ", "
            + str(self.start_page)
            + ", "
            + str(self.end_page)
            + ", "
            + str(self.number_of_pages)
            + ", "
            + str(self.doi)
            + ", "
            + str(self.link)
            + ", "
            + str(self.source)
        )
    

class IPublishing_Library(Base_Library):
    def __init__(self):
        Base_Library.__init__(self)
        self.description = None
        self.author_rus = None
        self.source = "iPublishing"

    def Print(self):
        return (
            str(self.author)
            + ", "
            + str(self.title)
            + ", "
            + str(self.year)
            + ", "
            + str(self.article)
            + ", "
            + str(self.link)
            + ", "
            + str(self.description)
            + ", "
            + str(self.doi)
            + ", "
            + str(self.source)
        )


class eLibrary(Base_Library):
    def __init__(self):
        Base_Library.__init__(self)
        self.id = None
        self.linkurl = None
        self.genre = None
        self.type = None
        self.id = None
        self.id = None
        self.id = None
        self.author_rus = None
        self.source = "eLibrary"