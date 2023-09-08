class Base_Library:
    def __init__(self):
        self.author = None
        self.title = None
        self.year = None
        self.article = None
        self.link = None


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
        self.doi = None
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

    def __eq__(self, other):
        if (
            self.author == other.author
            and self.title == other.title
            and self.article == other.article
            and self.year == other.year
            and self.link == other.link
            and self.source_name == other.source_name
            and self.doi == other.doi
        ):
            return True
        else:
            return False


class WOS_Library(Base_Library):
    def __init__(self):
        Base_Library.__init__(self)
        self.volume = None
        self.issue = None
        self.start_page = None
        self.end_page = None
        self.number_of_pages = None
        self.doi = None
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
        self.doi = None
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
