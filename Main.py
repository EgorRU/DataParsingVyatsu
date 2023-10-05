from GUI.Window import win

from psycopg2 import Error
import psycopg2
from config import PASSWD, create_bool


def create_bd():
    try:
        connection = psycopg2.connect(user="postgres",password=f"{PASSWD}",host="127.0.0.1",port="5432")
        connection.autocommit = True
        cursor = connection.cursor()
        cursor.execute("create tablespace project_tablespace location 'C:/sql';")
        cursor.execute("create database project_database tablespace project_tablespace;")
        cursor.execute("create schema project_schema;")
        create = '''
        CREATE TABLE IF NOT EXISTS project_schema.Article (
        WOS_ID text PRIMARY KEY NOT NULL,
        article_name text NOT NULL DEFAULT NULL,
        publication_year text NOT NULL DEFAULT NULL,
        volume text NULL DEFAULT NULL,
        issue text NULL DEFAULT NULL,
        start_page text NULL DEFAULT NULL,
        end_page text NULL DEFAULT NULL,
        DOI text NULL DEFAULT NULL,
        source_DOI text NULL DEFAULT NULL,
        include_RINC boolean NULL DEFAULT False,
        inclide_core_RINC boolean NULL DEFAULT False
        );
        
        CREATE TABLE IF NOT EXISTS project_schema.Journal (
        journal_name text PRIMARY KEY NOT NULL,
        ISSN text NULL DEFAULT NULL,
        eISSN text NULL DEFAULT NULL,
        ISBN text NULL DEFAULT NULL
        );
        
        CREATE TABLE IF NOT EXISTS project_schema.Authors (
        ORCID text PRIMARY KEY NOT NULL,
        FIO text NOT NULL DEFAULT NULL
        );
        
        CREATE TABLE IF NOT EXISTS project_schema.School (
        school_name text PRIMARY KEY NOT NULL,
        founder text NULL DEFAULT NULL,
        location text NULL DEFAULT NULL
        );'''
        cursor.execute(create)
        print("Таблицы успешно созданы")
    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Соединение с PostgreSQL закрыто")

def main():
    if create_bool==False:
        create_bd()
        data = ""
        with open("config.py",'r',encoding="utf-8") as file:
            data = file.readline()
        with open("config.py",'w',encoding="utf-8") as file:
            file.write(data)
            file.write("create_bool = True")
    else:
        print("Структура уже была создана")
    win.mainloop()
    

if __name__ == "__main__":
     main()

