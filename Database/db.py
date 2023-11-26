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
        global connection
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
        title text PRIMARY KEY,
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
        unique_wos_id text primary key not null,
        title_article text not null,
        year decimal(4,0) not null check(year>0 and year::integer<date_part('year', now())::integer+1),
        volume text,
        issue text,
        start_page text,
        end_page text,
        doi text,
        link text,
        number_article text,
        title text,
        foreign key (title)
        references project_schema.journal(title) 
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
        author text primary key not null,
        orcids text not null,
        school_name text,
        foreign key (school_name)
        references project_schema.school(school_name) 
        on delete set null on update cascade);

        '''
        cursor.execute(create)
        print("Таблица authors успешно создана")


        create = '''
        CREATE TABLE if not exists project_schema.article_authors(
        unique_wos_id text,
        author text,
        foreign key (unique_wos_id) 
        references project_schema.article(unique_wos_id) on delete cascade on update cascade,
        foreign key (author)
        references project_schema.authors(author) on delete cascade on update cascade,
        primary key (author, unique_wos_id));

        '''
        cursor.execute(create)
        print("Таблица article_authors успешно создана")


        create = '''
        CREATE TABLE if not exists project_schema.article_article(
        unique_wos_id text,
        unique_wos_id_ref text,
        foreign key (unique_wos_id)
        references project_schema.article(unique_wos_id) on delete cascade on update cascade,
        foreign key (unique_wos_id)
        references project_schema.article(unique_wos_id) on delete cascade on update cascade,
        primary key (unique_wos_id, unique_wos_id_ref));

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
        CREATE OR REPLACE FUNCTION project_schema.articles_in_journal(in title_func text, out count bigint)
        as $$
        select count(*) from project_schema.article a join project_schema.journal j
        on a.title = j.title where $1 = a.title_article;
        $$ language sql;

        '''
        cursor.execute(create)
        print("function citation_for_year успешно создана")


        create = '''
        CREATE OR REPLACE FUNCTION project_schema.count_articles_for_author(in author_func text, in title_func text, out count bigint)
        as $$
        select count(*) from project_schema.article a join project_schema.journal j on a.title = j.title 
        join project_schema.article_authors aru on a.unique_wos_id = aru.unique_wos_id 
        join project_schema.authors au on aru.author = au.author
        where $1 = au.author
        and $2 = a.title_article;
        $$ language sql;

        '''
        cursor.execute(create)
        print("function count_articles_for_author успешно создана")


        create = '''
        CREATE OR REPLACE VIEW project_schema.wos AS
        SELECT
        a.unique_wos_id,
        a.title_article, 
        a.year, 
        a.volume,
        a.issue,
        a.start_page,
        a.end_page,
        a.doi, 
        a.link, 
        j.title,
        a.number_article,
        au.author,
        au.orcids
        
        FROM project_schema.article a
        JOIN project_schema.journal j on a.title = j.title
        JOIN project_schema.article_authors aru on a.unique_wos_id = aru.unique_wos_id
        join project_schema.authors au on aru.author = au.author;

        '''
        cursor.execute(create)
        print("VIEW wos успешно создана")


        create = '''
        CREATE OR REPLACE function project_schema.insert_view_wos() returns trigger as $$
        begin
        if (select count(*) from 
        project_schema.article a 
        join project_schema.article_authors aru on a.unique_wos_id=aru.unique_wos_id 
        join project_schema.authors au on aru.author=au.author
        where a.title_article=new.title_article and au.author=new.author)=0
        then 
        if (select count(*) from project_schema.journal j where j.title=new.title)=0 then
        insert into project_schema.journal (title) values(new.title);
        end if;
        if (select count(*) from project_schema.authors a where a.author=new.author)=0 then
        insert into project_schema.authors (author, orcids) values(new.author, new.orcids);
        end if;
        if (select count(*) from project_schema.article a where a.unique_wos_id=new.unique_wos_id)=0 then
        insert into project_schema.article (unique_wos_id, title_article, year, volume, issue,
        start_page, end_page, doi, link, number_article, title) 
        values(new.unique_wos_id, new.title_article, new.year, new.volume, new.issue, 
        new.start_page, new.end_page, new.doi, new.link, new.number_article, new.title);
        end if;
        if (select count(*) from project_schema.article_authors aa where aa.author=new.author and aa.unique_wos_id=new.unique_wos_id)=0 then
        insert into project_schema.article_authors (author, unique_wos_id) values(new.author, new.unique_wos_id);
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
        if (select count(a.title_article) from project_schema.article a where a.title_article in (select a.title_article from project_schema.article a where a.unique_wos_id=old.unique_wos_id))=1 then
        delete from project_schema.journal j where j.title in (select a.title from project_schema.article a where a.unique_wos_id=old.unique_wos_id);
        end if;
        if (select count(aru.author) from project_schema.article_authors aru where aru.author=old.author)=1 then
        delete from project_schema.authors a where a.author=old.author;
        end if;
        if (select count(*) from project_schema.article a where a.unique_wos_id=old.unique_wos_id)>0 then
        DELETE from project_schema.article a where a.unique_wos_id=old.unique_wos_id;
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
                list_new[i].unique_wos_id,
                list_new[i].title_article,
                int(list_new[i].year) if list_new[i].year != "" else 0,
                list_new[i].volume,
                list_new[i].issue,
                list_new[i].start_page,
                list_new[i].end_page,
                list_new[i].doi,
                list_new[i].link,
                list_new[i].title,
                list_new[i].number_article,
                list_new[i].author,
                list_new[i].orcids
                )
            try:
                cursor.execute('INSERT INTO project_schema.wos values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)', article_tuple)
            except Exception as e:
                writeFile("info", "При добавлении новых данных возникла ошибка")
                writeFile("exception", f"{str(e)}", traceback.format_exc())
            
        #добавляем одинаковые
        for i in range(len(list_ident)):
            article_tuple = (
                list_ident[i].unique_wos_id,
                list_ident[i].title_article,
                int(list_ident[i].year) if list_ident[i].year != "" else 0,
                list_ident[i].volume,
                list_ident[i].issue,
                list_ident[i].start_page,
                list_ident[i].end_page,
                list_ident[i].doi,
                list_ident[i].link,
                list_ident[i].title,
                list_ident[i].number_article,
                list_ident[i].author,
                list_ident[i].orcids
            )
            try:
                cursor.execute('INSERT INTO project_schema.wos values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)', article_tuple)
            except Exception as e:
                writeFile("info", "При добавлении одинаковых данных возникла ошибка")
                writeFile("exception", f"{str(e)}", traceback.format_exc())
        
        #удаляем старые
        for i in range(len(list_remove)):
            article_tuple = (
                list_remove[i].unique_wos_id,
                list_remove[i].orcids
                )
            try:
                cursor.execute('DELETE from project_schema.wos where unique_wos_id=%s and orcids=%s', article_tuple)
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