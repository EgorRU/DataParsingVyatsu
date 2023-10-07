from GUI.Window import win
import os
import psycopg2
from psycopg2 import Error
from config import PASSWD


def create_bd():
    #подключаемся к базе данных postgres
    #создаём табличное простанство и базу данных в новом табличном пространстве
    try:
        connection = psycopg2.connect(user="postgres",password=f"{PASSWD}",host="127.0.0.1",port="5432")
        connection.autocommit = True
        cursor = connection.cursor()
        if not os.path.exists("C:/sql"): 
            os.mkdir("C:/sql")
        cursor.execute("create tablespace project_tablespace location 'C:/sql';")
        print("Табличное пространство успешно создано")
        cursor.execute("create database scopus tablespace project_tablespace;")
        cursor.execute("create database wos tablespace project_tablespace;")
        print("Базы данных успешно создана")
    except (Exception, Error) as error:
        print("[!] Ошибка при создании табличного пространства и базы данных PostgreSQL", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
    

    #подключаемся к новой базе данных scopus
    #создаём схему, таблицы, тригеры, функции и другие объекты бд
    try:
        connection = psycopg2.connect(user="postgres",password=f"{PASSWD}",host="127.0.0.1",port="5432", database="scopus")
        connection.autocommit = True
        cursor = connection.cursor()
        cursor.execute("create schema project_schema;")
        

        create = '''
        CREATE TABLE IF NOT EXISTS project_schema.Journal
        (
        journal_name text PRIMARY KEY NOT NULL,
        ISSN text,
        eISSN text,
        ISBN text
        );
        '''
        cursor.execute(create)
        print("Таблица Journal успешно создана")
        

        create = '''
        CREATE TYPE project_schema.state AS ENUM ('new', 'ident', 'old');
        '''
        cursor.execute(create)
        print("Enum state успешно создан")
        

        create = '''
        CREATE TABLE IF NOT EXISTS project_schema.Article
        (
        EID text PRIMARY KEY NOT NULL,
        article_name text NOT NULL,
        publication_year text NOT NULL,
        volume text,
        issue text,
        start_page text,
        end_page text,
        DOI text,
        citation text DEFAULT 0,
        include_RINC boolean DEFAULT False,
        inclide_core_RINC boolean DEFAULT False,
        statement project_schema.state NOT NULL,
        journal_name text,
        foreign key (journal_name)
        References project_schema.Journal(journal_name) 
        ON DELETE CASCADE ON UPDATE CASCADE
        );
        '''
        cursor.execute(create)
        print("Таблица Article успешно создана")
        

        create = '''
        CREATE TABLE IF NOT EXISTS project_schema.School
        (
        school_name text PRIMARY KEY NOT NULL,
        founder text,
        location text
        );
        '''
        cursor.execute(create)
        print("Таблица School успешно создана")
        
    
        create = '''
        CREATE TABLE IF NOT EXISTS project_schema.Authors
        (
        ORCID text PRIMARY KEY NOT NULL,
        FIO text NOT NULL,
        school_name text,
        foreign key (school_name)
        References project_schema.School(school_name) 
        ON DELETE CASCADE ON UPDATE CASCADE
        );
        '''
        cursor.execute(create)
        print("Таблица Authors успешно создана")
        

        create = '''
        CREATE TABLE IF NOT EXISTS project_schema.Article_Authors
        (
        EID text,
        ORCID text,
        foreign key (EID) 
        References project_schema.Article(EID) ON DELETE CASCADE ON UPDATE CASCADE,
        foreign key (ORCID)
        References project_schema.Authors(ORCID) ON DELETE CASCADE ON UPDATE CASCADE,
        primary key (ORCID, EID)
        );
        '''
        cursor.execute(create)
        print("Таблица Article_Authors успешно создана")
        

        create = '''
        CREATE TABLE IF NOT EXISTS project_schema.Article_Article
        (
        EID text,
        EID_ref text,
        foreign key (EID)
        References project_schema.Article(EID) ON DELETE CASCADE ON UPDATE CASCADE,
        foreign key (EID)
        References project_schema.Article(EID) ON DELETE CASCADE ON UPDATE CASCADE,
        primary key (EID, EID_ref)
        );
        '''
        cursor.execute(create)
        print("Таблица Article_Article успешно создана")
        

        create = '''
        create or replace function project_schema.count_per_year(in publication_year_func text, in state_func project_schema.state)
        returns bigint as $$
        BEGIN
        select count(*) from project_schema.Article a where publication_year_func = a.publication_year and state_func = a.statement;
        END;
        $$ language plpgsql;
        '''
        cursor.execute(create)
        print("function count_per_year успешно создана")
        

        create = '''
        create or replace function project_schema.citation_for_author_per_year (in FIO_func text, in publucation_year_func text, in state_func project_schema.state)
        returns bigint as $$
        BEGIN
        select sum (a.citation::integer) as sum_of_citation from project_schema.Article a join project_schema.Journal j 
        on a.journal_name = j.journal_name join project_schema.Article_Authors aru
        on a.EID = aru.EID join project_schema.Authors au 
        on aru.ORCID = au.ORCID where FIO_func = au.FIO
        and state_func = a.statement
        and publucation_year_func = a.publication_year;
        END;
        $$ language plpgsql;
        '''
        cursor.execute(create)
        print("function citation_for_author_per_year успешно создана")
        

        create = '''
        create or replace function project_schema.articles_in_journal_by_author (in FIO_func text, in journal_name_func text, in state_func project_schema.state)
        returns bigint as $$
        BEGIN
        select count(*) from project_schema.Article a join project_schema.Journal j 
        on a.journal_name = j.journal_name join project_schema.Article_Authors aru
        on a.EID = aru.EID join project_schema.Authors au 
        on aru.ORCID = au.ORCID
        where journal_name_func = a.journal_name 
        and FIO_func = au.FIO
        and state_func = a.statement;
        END;
        $$ language plpgsql;
        '''
        cursor.execute(create)
        print("function articles_in_journal_by_author успешно создана")
        
    except (Exception, Error) as error:
        print("[!] Ошибка при создании объектов базы данных scopus", error)
    finally:
        if connection:
            cursor.close()
            connection.close()



    #подключаемся к новой базе данных wos
    #создаём схему, таблицы, тригеры, функции и другие объекты бд
    try:
        connection = psycopg2.connect(user="postgres",password=f"{PASSWD}",host="127.0.0.1",port="5432", database="wos")
        connection.autocommit = True
        cursor = connection.cursor()
        cursor.execute("create schema project_schema;")
        

        create = '''
        CREATE TABLE IF NOT EXISTS project_schema.Journal
        (
        journal_name text PRIMARY KEY NOT NULL,
        ISSN text,
        eISSN text,
        ISBN text
        );
        '''
        cursor.execute(create)
        print("Таблица Journal успешно создана")
        

        create = '''
        CREATE TYPE project_schema.state AS ENUM ('new', 'ident', 'old');
        '''
        cursor.execute(create)
        print("Enum state успешно создан")
        

        create = '''
        CREATE TABLE IF NOT EXISTS project_schema.Article
        (
        WOS_ID text PRIMARY KEY NOT NULL,
        article_name text NOT NULL,
        publication_year text NOT NULL,
        volume text,
        issue text,
        start_page text,
        end_page text,
        DOI text,
        source_DOI text,
        include_RINC boolean DEFAULT False,
        inclide_core_RINC boolean DEFAULT False,
        statement project_schema.state NOT NULL,
        journal_name text,
        foreign key (journal_name)
        References project_schema.Journal(journal_name)
        ON DELETE CASCADE ON UPDATE CASCADE
        );
        '''
        cursor.execute(create)
        print("Таблица Article успешно создана")
        

        create = '''
        CREATE TABLE IF NOT EXISTS project_schema.School
        (
        school_name text PRIMARY KEY NOT NULL,
        founder text,
        location text
        );
        '''
        cursor.execute(create)
        print("Таблица School успешно создана")
        
    
        create = '''
        CREATE TABLE IF NOT EXISTS project_schema.Authors
        (
        ORCID text PRIMARY KEY NOT NULL,
        FIO text NOT NULL,
        school_name text,
        foreign key (school_name)
        References project_schema.School(school_name) 
        ON DELETE CASCADE ON UPDATE CASCADE
        );
        '''
        cursor.execute(create)
        print("Таблица Authors успешно создана")
        

        create = '''
        CREATE TABLE IF NOT EXISTS project_schema.Article_Authors
        (
        WOS_ID text,
        ORCID text,
        foreign key (WOS_ID)
        References project_schema.Article(WOS_ID) ON DELETE CASCADE ON UPDATE CASCADE,
        foreign key (ORCID)
        References project_schema.Authors(ORCID) ON DELETE CASCADE ON UPDATE CASCADE,
        primary key (ORCID, WOS_ID)
        );
        '''
        cursor.execute(create)
        print("Таблица Article_Authors успешно создана")
        

        create = '''
        CREATE TABLE IF NOT EXISTS project_schema.Article_Article
        (
        WOS_ID text,
        WOS_ID_ref text,
        foreign key (WOS_ID)
        References project_schema.Article(WOS_ID) ON DELETE CASCADE ON UPDATE CASCADE,
        foreign key (WOS_ID)
        References project_schema.Article(WOS_ID) ON DELETE CASCADE ON UPDATE CASCADE,
        primary key (WOS_ID, WOS_ID_ref)
        );
        '''
        cursor.execute(create)
        print("Таблица Article_Article успешно создана")
        

        create = '''
        create or replace function project_schema.count_per_year (in publication_year_func text, in state_func project_schema.state)
        returns bigint as $$
        BEGIN
        select count(*) from project_schema.Article a where publication_year_func = a.publication_year and state_func = a.statement;
        END;
        $$ language plpgsql;
        '''
        cursor.execute(create)
        print("function count_per_year успешно создана")
        

        create = '''
        create or replace function project_schema.articles_in_journal (in journal_name_func text, in state_func project_schema.state)
        returns bigint as $$
        BEGIN
        select count(*) from project_schema.Article a join project_schema.Journal j 
        on a.journal_name = j.journal_name where journal_name_func = a.journal_name 
        and state_func = a.statement;
        END;
        $$ language plpgsql;
        '''
        cursor.execute(create)
        print("function citation_for_author_per_year успешно создана")
        

        create = '''
        create or replace function project_schema.articles_in_journal_by_author (in FIO_func text, in journal_name_func text, in state_func project_schema.state)
        returns bigint as $$
        BEGIN
        select count(*) from project_schema.Article a join project_schema.Journal j 
        on a.journal_name = j.journal_name join Article_Authors aru
        on a.WOS_ID = aru.WOS_ID join Authors au 
        on aru.ORCID = au.ORCID
        where journal_name_func = a.journal_name 
        and FIO_func = au.FIO
        and state_func = a.statement;
        END;
        $$ language plpgsql;
        '''
        cursor.execute(create)
        print("function articles_in_journal_by_author успешно создана")

    except (Exception, Error) as error:
        print("[!] Ошибка при создании объектов базы данных", error)
    finally:
        if connection:
            cursor.close()
            connection.close()


def main():
    #пытаемся подключится к базе данных Scopus и изменить какие-то строки
    try:
        connection = psycopg2.connect(user="postgres",password=f"{PASSWD}",host="127.0.0.1",port="5432",database="scopus")
        print("[!] Успешно подключились к базе данных Scopus")
        connection.autocommit = True
        cursor = connection.cursor()
    #если не смогли подключится, то создаём структуру базы данных
    except (Exception, UnicodeDecodeError):
        create_bd()
    finally:
        print("[!] Соединение с PostgreSQL закрыто после всех действий")
        
    try:
        connection = psycopg2.connect(user="postgres",password=f"{PASSWD}",host="127.0.0.1",port="5432",database="wos")
        print("[!] Успешно подключились к базе данных Scopus")
        connection.autocommit = True
        cursor = connection.cursor()
    #если не смогли подключится, то создаём структуру базы данных
    except (Exception, UnicodeDecodeError):
        create_bd()
    finally:
        print("[!] Соединение с PostgreSQL закрыто после всех действий")
        
    win.mainloop()
    

if __name__ == "__main__":
     main()

