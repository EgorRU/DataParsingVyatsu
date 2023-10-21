import os
import psycopg2
from psycopg2 import Error
from Logging import writeFile
from config import PASSWD


def create_db():
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
        print("Базы данных успешно создана")
    except (Exception, Error) as e:
        writeFile("exception", f'{str(e)}')
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
        
        #journal_name - source_name
        create = '''
        CREATE TABLE if not exists project_schema.journal(
        journal_name text primary key not null,
        ISSN text,
        eISSN text);

        '''
        cursor.execute(create)
        print("Таблица journal успешно создана")
        
        
        create = '''
        CREATE TABLE if not exists project_schema.article(
        eid text primary key not null,
        title text not null,
        year decimal(4,0) not null check(year>0 and year::integer<date_part('year', now())::integer+1),
        doi text,
        link text,
        volume text,
        issue text,
        start_page text,
        end_page text,
        number_of_pages text,
        number_article text,
        access text,
        citation integer default 0,
        lang text,
        publication_stage text,
        type_document text,
        journal_name text,
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
        id_author text primary key not null,
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
        eid text,
        id_author text,
        foreign key (eid) 
        references project_schema.article(eid) on delete cascade on update cascade,
        foreign key (id_author)
        references project_schema.authors(id_author) on delete cascade on update cascade,
        primary key (id_author, eid));

        '''
        cursor.execute(create)
        print("Таблица article_authors успешно создана")
        

        create = '''
        CREATE TABLE if not exists project_schema.article_article(
        eid text,
        eid_ref text,
        foreign key (eid)
        references project_schema.article(eid) on delete cascade on update cascade,
        foreign key (eid)
        references project_schema.article(eid) on delete cascade on update cascade,
        primary key (eid, eid_ref));

        '''
        cursor.execute(create)
        print("Таблица article_article успешно создана")
        

        create = '''
        CREATE OR REPLACE FUNCTION project_schema.count_article_for_year(in year decimal(4,0), out count bigint)
        as $$
        select count(*) from project_schema.article a where $1 = a.year;
        $$ language sql;

        '''
        cursor.execute(create)
        print("function count_article_for_year успешно создана")
        

        create = '''
        CREATE OR REPLACE FUNCTION project_schema.citation_for_year(in year decimal(4,0), out count bigint)
        as $$
        select sum(a.citation) as sum_of_citation from project_schema.article a where $1 = a. year;
        $$ language sql;

        '''
        cursor.execute(create)
        print("function citation_for_year успешно создана")
        

        create = '''
        CREATE OR REPLACE FUNCTION project_schema.count_articles_for_author(in fio text, out count bigint)
        as $$
        select count(*) from project_schema.article a join project_schema.article_authors a_au
        on a.eid = a_au.eid join project_schema.authors au 
        on a_au.id_author = au.id_author
        where $1 = au.fio;
        $$ language sql;

        '''
        cursor.execute(create)
        print("function count_articles_for_author успешно создана")
        

        create = '''
        CREATE OR REPLACE VIEW project_schema.scopus AS
        SELECT  
        au.fio,
        a.title, 
        a.year, 
        a.doi, 
        a.link, 
        a.volume, 
        a.issue,
        a.start_page,
        a.end_page,
        a.number_of_pages,
        a.number_article,
        a.access,
        a.citation,
        a.eid,
        au.id_author,
        a.lang,
        a.publication_stage,
        a.journal_name,
        a.type_document
        FROM project_schema.article a
        JOIN project_schema.article_authors a_au on a.eid = a_au.eid
        join project_schema.authors au on a_au.id_author = au.id_author;

        '''
        cursor.execute(create)
        print("VIEW scopus успешно создана")
        

        create = '''
        CREATE OR REPLACE function project_schema.insert_view_scopus() returns trigger as $$
        begin
        if (select count(*) from 
        project_schema.article a 
        join project_schema.article_authors a_au on a.eid=a_au.eid 
        join project_schema.authors au on a_au.id_author=au.id_author
        where a.title=new.title and au.fio=new.fio)=0
        then 
        if (select count(*) from project_schema.journal j where j.journal_name=new.journal_name)=0 then
        insert into project_schema.journal (journal_name) values(new.journal_name);
        end if;
        if (select count(*) from project_schema.authors a where a.id_author=new.id_author)=0 then
        insert into project_schema.authors (id_author, fio) values(new.id_author, new.fio);
        end if;
        if (select count(*) from project_schema.article a where a.eid=new.eid)=0 then
        insert into project_schema.article (title, year, doi, link,
        volume, issue, start_page, end_page, number_of_pages, number_article, 
        access, citation, eid, lang, publication_stage, journal_name, type_document) 
        values(new.title, new.year, new.doi, new.link,
        new.volume, new.issue, new.start_page, new.end_page, new.number_of_pages, new.number_article, 
        new.access, new.citation, new.eid, new.lang, new.publication_stage, new.journal_name, new.type_document);
        end if;
        if (select count(*) from project_schema.article_authors aa where aa.id_author=new.id_author and aa.eid=new.eid)=0 then
        insert into project_schema.article_authors (id_author, eid) values(new.id_author, new.eid);
        end if;
        end if;
        return new;
        end;
        $$ language plpgsql;

        '''
        cursor.execute(create)
        print("FUNCTION insert_view_scopus успешно создана")
        
         
        create = '''
        CREATE OR REPLACE TRIGGER trigger_insert_scopus
        instead of insert on project_schema.scopus
        for each row
        execute function project_schema.insert_view_scopus();

        '''
        cursor.execute(create)
        print("TRIGGER trigger_insert_scopus успешно создан")


        create = '''
        CREATE OR REPLACE function project_schema.update_view_scopus() returns trigger as $$
        begin
        raise exception 'Lines cannot be updated';
        return old;
        end;
        $$ language plpgsql;
        '''
        cursor.execute(create)
        print("FUNCTION update_view_scopus успешно создана")
        
         
        create = '''
        CREATE OR REPLACE TRIGGER trigger_update_scopus
        instead of update on project_schema.scopus
        for each row
        execute function project_schema.update_view_scopus();
        '''
        cursor.execute(create)
        print("TRIGGER trigger_update_scopus успешно создан")
        

        create = '''
        CREATE OR REPLACE function project_schema.delete_view_scopus() returns trigger as $$
        begin
        if (select count(a.journal_name) from project_schema.article a where a.journal_name in (select a.journal_name from project_schema.article a where a.eid=old.eid))=1 then
        delete from project_schema.journal j where j.journal_name in (select a.journal_name from project_schema.article a where a.eid=old.eid);
        end if;
        if (select count(a_au.id_author) from project_schema.article_authors a_au where a_au.id_author=old.id_author)=1 then
        delete from project_schema.authors a where a.id_author=old.id_author;
        end if;
        if (select count(*) from project_schema.article a where a.eid=old.eid)>0 then
        DELETE from project_schema.article a where a.eid=old.eid;
        end if;
        return old;
        end;
        $$ language plpgsql;
        '''
        cursor.execute(create)
        print("FUNCTION update_view_scopus успешно создана")
        
         
        create = '''
        CREATE OR REPLACE TRIGGER trigger_delete_scopus
        instead of delete on project_schema.scopus
        for each row
        execute function project_schema.delete_view_scopus();
        '''
        cursor.execute(create)
        print("TRIGGER trigger_update_scopus успешно создан")
    except (Exception, Error) as e:
        writeFile("exception", f"{str(e)}")
    finally:
        if connection:
            cursor.close()
            connection.close()
        

            
def update_db(list_new, list_ident, list_remove):
    #поключаемся к базе данных
    try:
        connection = psycopg2.connect(user="postgres",password=f"{PASSWD}",host="127.0.0.1",port="5432",database="scopus")
        print("[!] Успешно подключились к базе данных Scopus")
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
                list_new[i].number_of_pages,
                list_new[i].number_article, 
		        list_new[i].access,
                list_new[i].citation,
                list_new[i].eid,
		        list_new[i].id_author,
                list_new[i].lang,
                list_new[i].publication_stage,
                list_new[i].source_name,
                list_new[i].type_document
                )
            try:
                cursor.execute('INSERT INTO project_schema.scopus values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)', article_tuple)
            except Exception as e:
                writeFile("exception", f"{str(e)}")
            
        #добавляем одинаковые
        for i in range(len(list_ident)):
            article_tuple = (
                list_ident[i].author,
                list_ident[i].title,
                int(list_ident[i].year) if list_ident[i].year!="" else 0,
                list_ident[i].doi,
                list_ident[i].link,
		        list_ident[i].volume,
                list_ident[i].issue,
                list_ident[i].start_page,
                list_ident[i].end_page,
                list_ident[i].number_of_pages,
                list_ident[i].number_article, 
		        list_ident[i].access,
                list_ident[i].citation,
                list_ident[i].eid,
		        list_ident[i].id_author,
                list_ident[i].lang,
                list_ident[i].publication_stage,
                list_ident[i].source_name,
                list_ident[i].type_document
                )
            try:
                cursor.execute('INSERT INTO project_schema.scopus values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)', article_tuple)
            except Exception as e:
                writeFile("exception", f"{str(e)}")
        
        #удаляем старые
        for i in range(len(list_remove)):
            article_tuple = (
                list_remove[i].eid,
                list_remove[i].id_author
                )
            cursor.execute('DELETE from project_schema.scopus where eid=%s and id_author=%s', article_tuple)
    except (Exception, Error) as e:
        writeFile("exception", f"{str(e)}")
    finally:
        if connection:
            print("[!] Успешно отключились от базы данных")
            cursor.close()
            connection.close()