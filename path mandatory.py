import os

def check_directory():
    directory_not_found: bool = True
    file_not_found: bool = True
    while directory_not_found:
        full_path = input("Please type the path to your file's directory:\n").lower()
        if os.path.exists(full_path):
            print("Ok, good! Such directory exists!")
            while file_not_found:
                file_name = os.path.join (full_path, input("Please type the file name:\n").lower())
                if os.path.isfile(file_name):
                    print ("Such file exists!")
                    break
                else:
                    print("Sorry, no such file in the directory you've mentioned. Please check the file name and try again")
                    continue
            else:
                return
            break
        else:
            print ("Sorry, your path doesn't exist. Are you sure it's correct one? Let's try all over again.")
            continue
    else:
        return

check_directory()