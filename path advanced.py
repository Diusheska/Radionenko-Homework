import os
import time

def check_directory():
    full_path = input("Please type the path to your file's directory:\n").lower()
    if os.path.exists(full_path):
        print("Ok, good! Such directory exists! Check out the files in it:")
        for root, dirs, files in os.walk(full_path):
            for filename in files:
                file_size = os.path.getsize(os.path.join(root, filename))
                created_date = time.ctime(os.path.getctime(os.path.join(root, filename)))
                modified_date = time.ctime(os.path.getmtime(os.path.join(root, filename)))
                print ("File name: {}, size (in bytes): {}, created date: {}, last modified date: {}".format(filename, file_size, created_date, modified_date))
    else:
        os.mkdir(full_path) # нет проверки на дурака - рассчет на то, что юхер ввел существующий диск, слєши и тп
        print ("Your path didn't exist, but I just created it for you - how cool it that?")
        
        
check_directory()

