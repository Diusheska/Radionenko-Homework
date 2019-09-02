import argparse
import os

def parse_path():
	parser = argparse.ArgumentParser(
	description='Please type the full path to directory and file name in it. The utilite will check if such directory and file in it exist')
	parser.add_argument("full_path", help = "Full path to your file")
	parser.add_argument("file_name", help = 'Filename (with extension) to look for in  "name.smth" format')
	args = parser.parse_args()
	return args

def search_dir (full_path, file_name):
  if os.path.exists(full_path):
      print("Such directory exists!")
      file_path = os.path.join (full_path, file_name.lower())
      if os.path.isfile(file_name):
        print ("And such file exists as well!")
      else:
        print("But there is no '{}' file in it.".format(file_name))
  else:
      print ("Sorry, your path doesn't exist.")
	
		  
if __name__== "__main__":
    args = parse_path()
    search_dir(args.full_path, args.file_name)
		  
