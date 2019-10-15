import argparse, pymongo, sqlite3


parser = argparse.ArgumentParser(description = "Arguments to create mongo db and its collections using tables in SQLite db")
parser.add_argument("-mongo_db", "--mongo_db_name", default = 'nadiia_test', help = "Name of the database to create in mongo")
parser.add_argument("-sql_db", "--sql_db_name", default = 'nadiia_test.db', help = "Name of the database to query in SQLite")
parser.add_argument("-col_1","--project_data_source", default = 'project', help = "Name of table in SQLlite to select data from. Will be also used as a name to create mongo collection. In this task - 'project' table")
parser.add_argument("-col_2","--tasks_data_source", default = 'tasks', help = "Name of table in SQLlite to select data from. Will be also used as a name to create mongo collection. In this task - 'tasks' table")
parser.add_argument("-id1","--id_in_collection1", default = 'Name', help = "Primary key in collection1 to be used as id")
parser.add_argument("-id2","--id_in_collection2", default = 'id', help = "Primary key in collection2 to be used as id")
args = parser.parse_args()


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


def insert_into_collection (mongo_db, collection1, collection2, data1, data2):
    my_collection1 = mongo_db[collection1]
    my_collection2 = mongo_db[collection2]
    my_collection1.insert_many(data1)
    my_collection2.insert_many(data2)


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

if __name__ == '__main__':
    my_client = set_up_mongo_connection()
    my_db = set_up_mongo_db(my_client, args.mongo_db_name)
    projects = create_collection(my_db, args.project_data_source)
    tasks = create_collection(my_db, args.tasks_data_source)
    conn = set_up_sql_connection(args.sql_db_name)
    project_table_data = get_project_data(conn)
    tasks_table_data = get_tasks_data(conn)
    proj_for_mongo = convert_sql_data(project_table_data, args.id_in_collection1)
    tasks_for_mongo = convert_sql_data(tasks_table_data, args.id_in_collection2)
    insert_into_collection (my_db, args.project_data_source, args.tasks_data_source, proj_for_mongo, tasks_for_mongo)
    aggregate_and_filter(my_db, args.project_data_source, args.tasks_data_source)
