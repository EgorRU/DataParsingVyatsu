import psycopg2
import traceback
from psycopg2 import Error
from Logging import writeFile
from config import PASSWD


connection = ""
def create_db():
    #подключаемся к базе данных postgres
    #создаём табличное простанство и базу данных в новом табличном пространстве
    try:
        connection = psycopg2.connect(user="postgres",password=f"{PASSWD}",host="127.0.0.1",port="5432")
        connection.autocommit = True
        cursor = connection.cursor()
        cursor.execute("create database wos tablespace project_tablespace;")
        print("Базы данных успешно создана")
    except (Exception, Error) as e:
        writeFile("info", "Проблема при создании табличного пространства")
        writeFile("exception", f'{str(e)}', traceback.format_exc())
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
        CREATE TABLE if not exists project_schema.journal(
        journal_name text PRIMARY KEY NOT NULL,
        ISSN text,
        eISSN text,
        ISBN text);

        '''
        cursor.execute(create)
        print("Таблица journal успешно создана")


        create = '''
        CREATE TYPE project_schema.state AS ENUM ('new', 'ok', 'old');

        '''
        cursor.execute(create)
        print("Enum state успешно создан")


        create = '''
        CREATE TABLE if not exists project_schema.article(
        wos_ID text primary key not null,
        article_name text not null,
        publication_year decimal(4,0) not null check(publication_year>0 and publication_year::integer<date_part('publication_year', now())::integer+1),
        volume text,
        issue text,
        start_page text,
        end_page text,
        DOI text,
        source_DOI text,
        include_RINC boolean,
        include_core_RINC boolean,
        statement state,
        journal_name text,
        title_article text,
        article_name text,
        foreign key (journal_name)
        references project_schema.journal(journal_name) 
        on delete set null on update cascade);

        '''
        cursor.execute(create)
        print("Таблица article успешно создана")


        create = '''
        CREATE TABLE if not exists project_schema.school(
        school_name text primary key not null,
        founder text,
        location text);

        '''
        cursor.execute(create)
        print("Таблица school успешно создана")


        create = '''
        CREATE TABLE if not exists project_schema.authors(
        ORCID text primary key not null,
        fio text not null,
        school_name text,
        foreign key (school_name)
        references project_schema.school(school_name) 
        on delete set null on update cascade);

        '''
        cursor.execute(create)
        print("Таблица authors успешно создана")


        create = '''
        CREATE TABLE if not exists project_schema.article_authors(
        wos_ID text,
        ORCID text,
        foreign key (wos_ID) 
        references project_schema.article(wos_ID) on delete cascade on update cascade,
        foreign key (ORCID)
        references project_schema.authors(ORCID) on delete cascade on update cascade,
        primary key (ORCID, wos_ID));

        '''
        cursor.execute(create)
        print("Таблица article_authors успешно создана")


        create = '''
        CREATE TABLE if not exists project_schema.article_article(
        wos_ID text,
        wos_ID_ref text,
        foreign key (wos_ID)
        references project_schema.article(wos_ID) on delete cascade on update cascade,
        foreign key (wos_ID)
        references project_schema.article(wos_ID) on delete cascade on update cascade,
        primary key (wos_ID, wos_ID_ref));

        '''
        cursor.execute(create)
        print("Таблица article_article успешно создана")


        create = '''
        CREATE OR REPLACE FUNCTION project_schema.count_article_for_year(in year decimal(4,0), out count bigint)
        as $$
        select count(*) from project_schema.article a where $1 = a.publication_year;
        $$ language sql;

        '''
        cursor.execute(create)
        print("function count_article_for_year успешно создана")


        create = '''
        CREATE OR REPLACE FUNCTION project_schema.articles_in_journal(in journal_name_func text, out count bigint)
        as $$
        select count(*) from project_schema.article a join project_schema.journal j
        on a.journal_name = j.journal_name where $1 = a.journal_name;
        $$ language sql;

        '''
        cursor.execute(create)
        print("function citation_for_year успешно создана")


        create = '''
        CREATE OR REPLACE FUNCTION project_schema.count_articles_for_author(in FIO_func text, in journal_name_func text, out count bigint)
        as $$
        select count(*) from project_schema.article a join project_schema.journal j on a.journal_name = j.journal_name 
        join project_schema.article_authors aru on a.wos_ID = aru.wos_ID 
        join project_schema.authors au on aru.ORCID = au.ORCID
        where $1 = au.fio
        and $2 = a.journal_name;
        $$ language sql;

        '''
        cursor.execute(create)
        print("function count_articles_for_author успешно создана")


        create = '''
        CREATE OR REPLACE VIEW project_schema.wos AS
        SELECT  
        au.fio,
        a.article_name, 
        a.publication_year, 
        a.doi, 
        a.source_DOI, 
        a.volume, 
        a.issue,
        a.start_page,
        a.end_page,
        a.number_article,
        a.number_article,
        au.ORCID,
        j.journal_name,
        FROM project_schema.article a
        JOIN project_schema.journal j on a.journal_name = j.journal_name
        JOIN project_schema.article_authors aru on a.wos_ID = aru.wos_ID
        join project_schema.authors au on aru.ORCID = au.ORCID;

        '''
        cursor.execute(create)
        print("VIEW wos успешно создана")


        create = '''
        CREATE OR REPLACE function project_schema.insert_view_wos() returns trigger as $$
        begin
        if (select count(*) from 
        project_schema.article a 
        join project_schema.article_authors aru on a.wos_ID=aru.wos_ID 
        join project_schema.authors au on aru.ORCID=au.ORCID
        where a.title=new.title and au.fio=new.fio)=0
        then 
        if (select count(*) from project_schema.journal j where j.journal_name=new.journal_name)=0 then
        insert into project_schema.journal (journal_name) values(new.journal_name);
        end if;
        if (select count(*) from project_schema.authors a where a.ORCID=new.ORCID)=0 then
        insert into project_schema.authors (ORCID, fio) values(new.ORCID, new.fio);
        end if;
        if (select count(*) from project_schema.article a where a.wos_ID=new.wos_ID)=0 then
        insert into project_schema.article (title, year, doi, link,
        volume, issue, start_page, end_page, number_of_pages, number_article, 
        access, citation, wos_ID, lang, publication_stage, journal_name, type_document) 
        values(new.title, new.year, new.doi, new.link,
        new.volume, new.issue, new.start_page, new.end_page, new.number_of_pages, new.number_article, 
        new.access, new.citation, new.wos_ID, new.lang, new.publication_stage, new.journal_name, new.type_document);
        end if;
        if (select count(*) from project_schema.article_authors aa where aa.ORCID=new.ORCID and aa.wos_ID=new.wos_ID)=0 then
        insert into project_schema.article_authors (ORCID, wos_ID) values(new.ORCID, new.wos_ID);
        end if;
        end if;
        return new;
        end;
        $$ language plpgsql;

        '''
        cursor.execute(create)
        print("FUNCTION insert_view_wos успешно создана")


        create = '''
        CREATE OR REPLACE TRIGGER trigger_insert_wos
        instead of insert on project_schema.wos
        for each row
        execute function project_schema.insert_view_wos();

        '''
        cursor.execute(create)
        print("TRIGGER trigger_insert_wos успешно создан")


        create = '''
        CREATE OR REPLACE function project_schema.update_view_wos() returns trigger as $$
        begin
        raise exception 'Lines cannot be updated';
        return old;
        end;
        $$ language plpgsql;
        
        '''
        cursor.execute(create)
        print("FUNCTION update_view_wos успешно создана")


        create = '''
        CREATE OR REPLACE TRIGGER trigger_update_wos
        instead of update on project_schema.wos
        for each row
        execute function project_schema.update_view_wos();
        
        '''
        cursor.execute(create)
        print("TRIGGER trigger_update_wos успешно создан")


        create = '''
        CREATE OR REPLACE function project_schema.delete_view_wos() returns trigger as $$
        begin
        if (select count(a.journal_name) from project_schema.article a where a.journal_name in (select a.journal_name from project_schema.article a where a.wos_ID=old.wos_ID))=1 then
        delete from project_schema.journal j where j.journal_name in (select a.journal_name from project_schema.article a where a.wos_ID=old.wos_ID);
        end if;
        if (select count(aru.ORCID) from project_schema.article_authors aru where aru.ORCID=old.ORCID)=1 then
        delete from project_schema.authors a where a.ORCID=old.ORCID;
        end if;
        if (select count(*) from project_schema.article a where a.wos_ID=old.wos_ID)>0 then
        DELETE from project_schema.article a where a.wos_ID=old.wos_ID;
        end if;
        return old;
        end;
        $$ language plpgsql;
        
        '''
        cursor.execute(create)
        print("FUNCTION update_view_wos успешно создана")


        create = '''
        CREATE OR REPLACE TRIGGER trigger_delete_wos
        instead of delete on project_schema.wos
        for each row
        execute function project_schema.delete_view_wos();
        
        '''
        cursor.execute(create)
        print("TRIGGER trigger_update_wos успешно создан")
    except (Exception, Error) as e:
        writeFile("info", "Проблема при создании таблиц, функций, тригеров, представлений")
        writeFile("exception", f"{str(e)}", traceback.format_exc())
    finally:
        if connection:
            print("[!] Соединение с базой данных закрыто")
            cursor.close()
            connection.close()
        
            
def update_db(list_new, list_ident, list_remove):
    #поключаемся к базе данных
    try:
        connection = psycopg2.connect(user="postgres",password=f"{PASSWD}",host="127.0.0.1",port="5432",database="wos")
        print("[!] Успешно подключились к базе данных wos")
        connection.autocommit = True
        cursor = connection.cursor()
        #заносим новые данные в бд
        for i in range(len(list_new)):
            article_tuple = (
                list_new[i].author,
                list_new[i].title,
                int(list_new[i].year) if list_new[i].year!="" else 0,
                list_new[i].doi,
                list_new[i].link,
                list_new[i].volume,
                list_new[i].issue,
                list_new[i].start_page,
                list_new[i].end_page,
                list_new[i].number_article,
                list_new[i].ORCIDs,
                list_new[i].title_article
                )
            try:
                cursor.execute('INSERT INTO project_schema.wos values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)', article_tuple)
            except Exception as e:
                writeFile("info", "При добавлении новых данных возникла ошибка")
                writeFile("exception", f"{str(e)}", traceback.format_exc())
            
        #добавляем одинаковые
        for i in range(len(list_ident)):
            article_tuple = (
                list_ident[i].author,
                list_ident[i].title,
                int(list_ident[i].year) if list_ident[i].year != "" else 0,
                list_ident[i].doi,
                list_ident[i].link,
                list_ident[i].volume,
                list_ident[i].issue,
                list_ident[i].start_page,
                list_ident[i].end_page,
                list_ident[i].number_article,
                list_ident[i].ORCIDs,
                list_ident[i].title_article
                )
            try:
                cursor.execute('INSERT INTO project_schema.wos values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)', article_tuple)
            except Exception as e:
                writeFile("info", "При добавлении одинаковых данных возникла ошибка")
                writeFile("exception", f"{str(e)}", traceback.format_exc())
        
        #удаляем старые
        for i in range(len(list_remove)):
            article_tuple = (
                list_remove[i].wos_ID,
                list_remove[i].ORCID
                )
            try:
                cursor.execute('DELETE from project_schema.wos where wos_ID=%s and ORCID=%s', article_tuple)
            except Exception as e:
                writeFile("info", "При удалении одинаковых данных возникла ошибка")
                writeFile("exception", f"{str(e)}", traceback.format_exc())
                
    except (Exception, Error) as e:
        writeFile("info", "При работе с базой данных возникла ошибка")
        writeFile("exception", f"{str(e)}", traceback.format_exc())
    finally:
        if connection:
            print("[!] Соединение с базой данных закрыто")
            cursor.close()
            connection.close()