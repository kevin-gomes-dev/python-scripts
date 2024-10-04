# Here will be rename functions. Simply call the function with the file
import os
import sys

# Put the string given before files
# Or remove string wherever found in files
# TODO: If list of strings, add list of strings sequentially. Or remove all strings found in list
def rename_files(directory=None,string=None,mode="yes"):
    directory = os.path.normpath(os.path.realpath(directory))
    if not directory:
        print("No directory")
        return
    if not string:
        print("No string")
        return
    file_list = os.walk(directory)
    for i,j,k in file_list:
        if k:
            for file in k:
                file = str(file)
                
                if mode == "yes":
                    # Rename k to string + what it is, or prepend it.
                    new_name = string + file
                elif mode == "no":
                    # Remove the found string in the filename
                    new_name = file.replace(string,"")
                else:
                    print("Mode given was " + str(mode) + ", not yes or no. Ending without renaming.")
                    return
                file_from = os.path.join(i,file)
                file_to = os.path.join(i,new_name)
                print("Before: " + str(file_from))
                print("After: " + str(file_to))
                print()
                os.rename(file_from,file_to)
                    
      
def main():
    args = sys.argv
    if len(args) <= 3:
        print ("Didn't supply enough args. Expects [dir,string,mode]")
        return
    args = args[1:]
    try:
        rename_files(args[0],args[1],args[2])
    except:
        print("exception")
        raise
  
main()