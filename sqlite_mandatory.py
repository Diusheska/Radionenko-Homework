# to rum this code in cmd you need to provide the following arguments:
# - db db_file_name, -csv1 path_to_csv_file_with_projects_data, -csv2 path_to_csv_file_with_tasks_data, -col name_of_project_to_filter_by

import argparse, os.path, csv, sqlite3, codecs
from prettytable import PrettyTable

parser = argparse.ArgumentParser(description = "Arguments to create db, create and populate tables in this db from csv files and print values from a table with given condition")
parser.add_argument("-db", "--db_file_name", help = "Name of the database to create tables in")
parser.add_argument("-csv1","--project_data_source", help = "CSV file with project data to insert into Project table")
parser.add_argument("-csv2","--tasks_data_source", help = "CSV file with tasks data to insert into Tasks table")
parser.add_argument("-col","--project_name", help = "Project name to use as a predicate")
args = parser.parse_args()


def create_database (db_file_name):
    db_exists = os.path.exists(db_file_name)
    if db_exists:
        print("Such db name exists. I'll delete it and create a new one")
        os.remove(db_file_name)
        conn = sqlite3.connect(db_file_name)
        return conn
    else:
        conn = sqlite3.connect(db_file_name)
        return conn


def create_tables(conn):
    curs = conn.cursor()
    curs.executescript("""
                CREATE TABLE Project
                (Name TEXT PRIMARY KEY,
                Description TEXT,
                Deadline DATE);

                CREATE TABLE Tasks
                (id NUMBER PRIMARY KEY,
                priority INTEGER,
                details TEXT,
                status TEXT,
                completed DATE,
                deadline DATE,
                project TEXT)""")
    conn.commit()


def populate_tables (conn, csv1, csv2):
    curs = conn.cursor()
    with codecs.open(csv1, encoding='utf-8') as project_data_source, codecs.open(csv2, encoding='utf-8') as tasks_data_source:
        dr_proj = csv.DictReader(project_data_source)
        dr_tasks = csv.DictReader(tasks_data_source)
        to_db_proj = [(i['name'], i['description'], i['deadline']) for i in dr_proj]
        to_db_tasks = [(i['id'] , i['priority'], i['details'], i['status'], i['deadline'], i['completed'], i['project']) for i in dr_tasks]
    for i in to_db_proj:
        curs.execute("INSERT INTO Project (name, description, deadline) VALUES (?, ?, ?)", i)
    for j in to_db_tasks:
        curs.execute("INSERT INTO Tasks (id, priority, details, status, deadline, completed, project) VALUES (?,?,?,?,?,?,?)", j)
        conn.commit()


def select_from_tables (conn, project_name):
    curs = conn.cursor()
    curs.execute("""
			SELECT p.name as project_name, t.id, t.priority, t.details, t.status, t.deadline, t.completed 
			FROM Project p 
				LEFT JOIN Tasks t  ON p.name = t.project
			WHERE p.name = ?""", [project_name]) # there might be projects without tasks
    result_set = curs.fetchall()
    col_names = [i[0] for i in curs.description]
    table_to_display = PrettyTable(col_names)
    for row in result_set:
        table_to_display.add_row(list(row))
    print(table_to_display)
    conn.close()


if __name__ == '__main__':
    conn = create_database(args.db_file_name)
    create_tables(conn)
    populate_tables(conn, args.project_data_source, args.tasks_data_source)
    select_from_tables(conn, args.project_name)
