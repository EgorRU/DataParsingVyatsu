class Base_Library:
    def __init__(self):
        self.author = ""
        self.original_author = ""
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
        self.number_article = ""
        self.start_page = ""
        self.end_page = ""
        self.number_of_pages = ""
        self.citation = 0
        self.doi = ""
        self.link = ""
        self.eid = ""
        self.access = ""
        self.publication_stage = ""
        self.type_document = ""
        self.lang = ""
        self.source = "Scopus"


class WOS_Library(Base_Library):
    def __init__(self):
        Base_Library.__init__(self)
        self.volume = ""
        self.issue = ""
        self.number_article = ""
        self.title_article = ""
        self.start_page = ""
        self.end_page = ""
        self.doi = ""
        self.link = ""
        self.conference_title = ""
        self.conference_date = ""
        self.conference_location = ""
        self.researcher_ids = ""
        self.orcids = ""
        self.issn = ""
        self.eissn = ""
        self.unique_wos_id = ""
        self.citations = 0
        self.document_type = ""
        self.source = "WOS"
  

class eLibrary_Library(Base_Library):
    def __init__(self):
        Base_Library.__init__(self)
        self.link = ""
        self.doi = ""
        self.id = ""
        self.type = ""
        self.citation = 0
        self.pages = ""
        self.volume = ""
        self.issn = ""
        self.eissn = ""
        self.title_article = ""
        self.publisher = ""
        self.country = ""
        self.grnti_code = ""
        self.number = ""
        self.source = "eLibrary"
    

class IPublishing_Library(Base_Library):
    def __init__(self):
        Base_Library.__init__(self)
        self.title_article = ""
        self.link = ""
        self.doi = ""
        self.institute = ""
        self.faculty = ""
        self.cathedra = ""
        self.full_bibliographic_description = ""
        self.cod_oecd = ""
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