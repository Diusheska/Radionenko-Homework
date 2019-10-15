import pymongo
import sqlite3


def set_up_mongo_connection():
    my_client = pymongo.MongoClient("mongodb://localhost:27017/")
    return my_client


def set_up_mongo_db(connection, db_name):
    db_list = connection.list_database_names()
    if db_name in db_list:
        connection.drop_database(db_name)
        my_db = connection[db_name]
    else:
        my_db = connection[db_name]
    return my_db


def create_collection(mongo_db, coll):
    collection = mongo_db[coll]
    return collection


def set_up_sql_connection(db_name):
    conn = sqlite3.connect(db_name)
    return conn


def get_project_data(conn):
    curs = conn.cursor()
    project_table_data = curs.execute("select * from project")
    #print (curs.fetchall())
    return project_table_data


def get_tasks_data(conn):
    curs2 = conn.cursor()
    tasks_table_data = curs2.execute("select * from tasks")
    return tasks_table_data


def convert_sql_data (sql_data, column_name):
    headers = [element[0] for element in sql_data.description]
    header_to_id = [header.replace(column_name, '_id') for header in headers]
    for_mongo = [{k: v for k, v in zip(header_to_id, row)} for row in sql_data]
    return for_mongo


def insert_into_collection (collection1, collection2, data1, data2):
    collection1.insert_many(data1)
    collection2.insert_many(data2)


def aggregate_and_filter(my_db, collection1, collection2):
    my_collection1 = my_db[collection1]
    result_set = my_collection1.aggregate([{
    "$lookup": {
      "from": collection2,
      "localField": "_id",
      "foreignField": "project",
      "as": "results"
    }
  },
  {
    "$unwind": "$results"
  },
  {
    "$match": {
      "results.status": "Cancelled"
    }
  },
  {
    "$project": {
      "_id": 1
    }
  }
])
    for i in result_set:
        print(i)


my_client = set_up_mongo_connection()
my_db = set_up_mongo_db(my_client, r'nadiia_test')
projects = create_collection(my_db, 'projects')
tasks = create_collection(my_db, 'tasks')
conn = set_up_sql_connection(r'nadiia_test.db')
project_table_data = get_project_data(conn)
tasks_table_data = get_tasks_data(conn)
proj_for_mongo = convert_sql_data(project_table_data, "Name")
tasks_for_mongo = convert_sql_data(tasks_table_data, "id")
insert_into_collection (projects, tasks, proj_for_mongo, tasks_for_mongo)
aggregate_and_filter(my_db, 'projects', 'tasks')
