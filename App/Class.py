class Base_Library:
    def __init__(self):
        self.author = None
        self.title = None
        self.year = None
        self.clear_author = None
        self.clear_title = None


class Scopus_Library(Base_Library):
    def __init__(self):
        Base_Library.__init__(self)
        self.id_author = None
        self.source_name = None
        self.volume = None
        self.issue = None
        self.article = None
        self.start_page = None
        self.end_page = None
        self.number_of_pages = None
        self.citation = None
        self.doi = None
        self.link = None
        self.source = "Scopus"

    def Print(self):
        return (
            str(self.author)
            + ", "
            + str(self.title)
            + ", "
            + str(self.year)
            + ", "
            + str(self.link)
            + ", "
            + str(self.citation)
            + ", "
            + str(self.doi)
            + ", "
            + str(self.clear_author)
            + ", "
            + str(self.clear_title)
        )


class WOS_Library(Base_Library):
    def __init__(self):
        Base_Library.__init__(self)
        self.volume = None
        self.issue = None
        self.article = None
        self.start_page = None
        self.end_page = None
        self.doi = None
        self.link = None
        self.conference_title = None
        self.conference_date = None
        self.conference_location = None
        self.researcher_ids = None
        self.ORCIDs = None
        self.ISSN = None
        self.eISSN = None
        self.unique_wos_id = None
        self.source = "WOS"

    def Print(self):
        return (
            str(self.author)
            + ", "
            + str(self.title)
            + ", "
            + str(self.year)
            + ", "
            + str(self.link)
            + ", "
            + str(self.doi)
            + ", "
            + str(self.clear_author)
            + ", "
            + str(self.clear_title)
        )
    

class eLibrary_Library(Base_Library):
    def __init__(self):
        Base_Library.__init__(self)
        self.link = None
        self.doi = None
        self.id = None
        self.type = None
        self.citation = None
        self.pages = None
        self.volume = None
        self.issn = None
        self.eissn = None
        self.title_journal = None
        self.publisher = None
        self.country = None
        self.GRNTI_code = None
        self.source = "eLibrary"

    def Print(self):
        return (
            str(self.author)
            + ", "
            + str(self.title)
            + ", "
            + str(self.year)
            + ", "
            + str(self.link)
            + ", "
            + str(self.doi)
            + ", "
            + str(self.clear_author)
            + ", "
            + str(self.clear_title)
        )
    

class IPublishing_Library(Base_Library):
    def __init__(self):
        Base_Library.__init__(self)
        self.author_rus = None
        self.article = None
        self.link = None
        self.description = None
        self.doi = None
        self.institute = None
        self.faculty = None
        self.cathedra = None
        self.full_bibliographic_description = None
        self.cod_OECD = None
        self.group_of_scientific_specialties = None
        self.GRNTI_code = None
        self.quartile_wos = None
        self.quartile_scopus = None
        self.quartile_scopus_sjr = None
        self.impact_factor_wos = None
        self.impact_factor_scopus = None
        self.impact_factor_elibrary_5_year = None
        self.impact_factor_elibrary_2_year = None
        self.source = "iPublishing"

    def Print(self):
        return (
            str(self.author)
            + ", "
            + str(self.title)
            + ", "
            + str(self.year)
            + ", "
            + str(self.link)
            + ", "
            + str(self.doi)
            + ", "
            + str(self.clear_author)
            + ", "
            + str(self.clear_title)
        )