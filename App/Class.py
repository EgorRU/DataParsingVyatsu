class Base_Library:
    def __init__(self):
        self.author = ""
        self.title = ""
        self.year = ""
        self.clear_author = ""
        self.clear_title = ""


class Scopus_Library(Base_Library):
    def __init__(self):
        Base_Library.__init__(self)
        self.id_author = ""
        self.source_name = ""
        self.volume = ""
        self.issue = ""
        self.article = ""
        self.start_page = ""
        self.end_page = ""
        self.number_of_pages = ""
        self.citation = 0
        self.doi = ""
        self.link = ""
        self.source = "Scopus"


class WOS_Library(Base_Library):
    def __init__(self):
        Base_Library.__init__(self)
        self.volume = ""
        self.issue = ""
        self.article = ""
        self.start_page = ""
        self.end_page = ""
        self.doi = ""
        self.link = ""
        self.conference_title = ""
        self.conference_date = ""
        self.conference_location = ""
        self.researcher_ids = ""
        self.ORCIDs = ""
        self.ISSN = ""
        self.eISSN = ""
        self.unique_wos_id = ""
        self.citations = 0
        self.document_type = ""
        self.source = "WOS"
  

class eLibrary_Library(Base_Library):
    def __init__(self):
        Base_Library.__init__(self)
        self.origin_author = ""
        self.link = ""
        self.doi = ""
        self.id = ""
        self.type = ""
        self.citation = 0
        self.pages = ""
        self.volume = ""
        self.issn = ""
        self.eissn = ""
        self.title_journal = ""
        self.publisher = ""
        self.country = ""
        self.GRNTI_code = ""
        self.source = "eLibrary"
    

class IPublishing_Library(Base_Library):
    def __init__(self):
        Base_Library.__init__(self)
        self.origin_author = ""
        self.article = ""
        self.link = ""
        self.doi = ""
        self.institute = ""
        self.faculty = ""
        self.cathedra = ""
        self.full_bibliographic_description = ""
        self.cod_OECD = ""
        self.group_of_scientific_specialties = ""
        self.GRNTI_code = ""
        self.quartile_wos = ""
        self.quartile_scopus = ""
        self.quartile_scopus_sjr = ""
        self.impact_factor_wos = ""
        self.impact_factor_scopus = ""
        self.impact_factor_elibrary_5_year = ""
        self.impact_factor_elibrary_2_year = ""
        self.source = "iPublishing"