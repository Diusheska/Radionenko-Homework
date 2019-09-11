import argparse, pypyodbc, json


def parse_path():
    parser = argparse.ArgumentParser(
    description = "Type path to .sql file. CREATE TABLE and INSERT statements from this file will be executed to create new table (if doesn't exist yet) in MS SQLServer")
    parser.add_argument("sql_path", help = "Full path to .sql file")
    parser.add_argument("server_name", help = "Your MSSQL Server name")
    parser.add_argument("db_name", help = "Name of db where you want new table created or where this table exists")
    args = parser.parse_args()
    return args.sql_path, args.server_name, args.db_name


def read_sql(sql_path):
    with open(sql_path, 'r', encoding="utf-8") as script_file:
        script_to_use=" ".join(line.rstrip() for line in script_file)
        return script_to_use


def set_up_connection(server_name, db_name, script_to_run):
    connection = pypyodbc.connect("Driver={SQL Server};"
                                  "Server=%s;"
                                  "Database=%s;"
                                  "Trusted_Connection=yes;" % (server_name, db_name))
    cursor = connection.cursor()
    cursor_results = cursor.execute(script_to_run)
    print (tuple(db_name))
    return cursor_results


def read_query_results(result_set):
    headers = [element[0] for element in result_set.description]
    data_to_convert = []
    for row in result_set:
        row_to_dict = {k: v for k, v in zip(headers, row) if k != 'password'}
        data_to_convert.append(row_to_dict)
    return data_to_convert


def convert_to_json(data_to_convert):
    output_json = json.dumps(data_to_convert, sort_keys = True, indent = 4)
    print(output_json)


if __name__== "__main__":
   sql_path, server_name, db_name = parse_path()
   script_to_use = read_sql(sql_path)
   cursor_results = set_up_connection(server_name, db_name, script_to_use)
   data_to_convert = read_query_results(cursor_results)
   convert_to_json(data_to_convert)
