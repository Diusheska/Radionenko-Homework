import argparse
import itertools
import csv
import re


def parse_path():
   parser = argparse.ArgumentParser(
   description = "You can type path to .csv file + column and get a list of values from that column")
   parser.add_argument("csv_path", help = "Full path to csv file")
   parser.add_argument("col_name", help = "Column header", nargs= "+")
   args = parser.parse_args()
   # next 2 lines will join space-separate arguments for column names, replace spaces with '_' and set to lowercase
   column_joined = '_'.join(args.col_name)
   column_fix_spaces = re.sub(r"\s+", '_', column_joined).lower() 
   return args.csv_path, column_fix_spaces


def lower_first(iterator):
    return itertools.chain([re.sub(r"\s+", '_',next(iterator)).lower()], iterator) # we'll use this function to set csv headers to lower and replace whitespaces with '_'


def read_csv (csv_file_path, column_name):
    with open(csv_file_path, 'r') as csv_file:
        reader = csv.DictReader(lower_first(csv_file))
        for row in reader:
            print (row[column_name])
                    

if __name__== "__main__":
   csv_path, column_fix_spaces = parse_path()
   read_csv(csv_path, column_fix_spaces)
