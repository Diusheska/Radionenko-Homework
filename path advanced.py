import argparse
import os
import time

def parse():
	parser = argparse.ArgumentParser(
	description='Please type the directory name. You will see the path and file name with specified extension, i.e .txt')
	parser.add_argument("-drive", "full_path", help = "Full path to your file")
	args = parser.parse_args()
	return args

def search_dir (full_path):
  if os.path.exists(full_path):
      print("Ok, good! Such directory exists! Check out the files in it:")
      for root, dirs, files in os.walk(full_path):
          for filename in files:
              file_size = os.path.getsize(os.path.join(root, filename))
              created_date = time.ctime(os.path.getctime(os.path.join(root, filename)))
              modified_date = time.ctime(os.path.getmtime(os.path.join(root, filename)))
              print ("File name: {}, size (in bytes): {}, created date: {}, last modified date: {}".format(filename, file_size, created_date, modified_date))
  else:
      # before creating a new directory, check if disk exists and if path syntax is correct
      drives_letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
      existing_drives = ['%s:' % d for d in drives_letters if os.path.exists('%s:' % d)]
      root_drive = os.path.splitdrive(full_path)[0].upper() # extract the first directory from the path (=drive)
      if root_drive in existing_drives:
          os.mkdir(full_path)
          print ("Your path didn't exist, but I just created it for you - how cool it that?")
      else:
          print ("Sorry, I wanted to create a directory for you, but I need a valid drive name")

		  
if __name__== "__main__":
    args = parse()
    search_dir(args.full_path)
		  
