import argparse, csv, json


def parse_path():
   parser = argparse.ArgumentParser(
   description = "You can type path to .csv file, path to .json file + column to obfuscate, and get csv data written into json")
   parser.add_argument("csv_path", help = "Full path to csv file")
   parser.add_argument("col_name", help = "Name of the column to skip in json")
   args = parser.parse_args()
   return args.csv_path, args.col_name


def skip_column(csv_row, column_to_skip):
   return {column_name: csv_row[column_name] for column_name in set(list(csv_row.keys())) if column_name != column_to_skip}  # returns new dictionary skipping pairs where key = column we want to skip


def read_csv (csv_file_path, column_to_skip):
    with open(csv_file_path, 'r') as csv_file:
        csv_reader = [dict(row) for row in csv.DictReader(csv_file)] # read each csv row as dictionary
        dict_to_convert = [skip_column(dict_row, column_to_skip) for dict_row in csv_reader] # apply a function to skip the column we don't want to show in JSON
        return dict_to_convert # this is dictionary made of csv data excluding the column we wanted to skip


def convert_to_json(csv_data):
	output_json = json.dumps(csv_data, sort_keys = True, indent = 4)
	print(output_json)

	
if __name__== "__main__":
   csv_path, col_name = parse_path()
   dict_to_convert = read_csv(csv_path, col_name)
   convert_to_json (dict_to_convert)
