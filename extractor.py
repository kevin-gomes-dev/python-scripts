# Cross platform and handles unique utf-8 filenames. Does not handle duplicate filenames (won't move)
# Extract all files of a certain type from the path given as well as all subfolders. They are extracted at the other path given.
# All original paths are put in a file to be able to undo this and restore their paths. The subfolders will not be deleted.
# That way we can keep moving stuff and have a running list of all the moves to reverse more than once
# Use bytes instead of strings for utf-8 encoding (many artists not in English, special characters in song names, etc.)
# TODO: Add either text interface for options, changing exts, reverse/move, etc. OR create a gui with buttons for this. See QtWidget?

# Created by Kevin Gomes

import os

def checkDirectories(baseFolder = "",extractToFolder = ""):
    if not (os.path.isdir(baseFolder) and os.path.isdir(extractToFolder)):
        return False
    return True
    
# Create txt file of all moves if doesn't exist in specified diretory
# Returns the file path in both cases
# Rewrite to use try except instead of ifs? Handle FileExistsError
def createMoves(dir):
    # Actual directory?
    if os.path.isdir(dir):
        file = os.path.join(dir,"moves.txt")
    # Does the file already exist?
    if os.path.isfile(file):
        return file
    fp = open(file,"x")
    fp.close()
    return file
        
# Write to file the path we came from, and the new path in the form [comeFrom,goTo]. This includes the file name for easy moving/renaming
# Assumes the file is open for +ba, fp should have access to .close, .write, etc
# Only write if the comeFrom + goTo pair are not already in, otherwise return nothing (We've moved here before, so we don't need duplicates)
# What if file is huge, GBs and can't fit in memory? Change to a for loop to go line by line, horribly inefficient.
def writeMove(fp,comeFrom,goTo):
    newLine = bytes(os.linesep,"utf-8")
    writeLine = comeFrom + newLine + goTo + newLine
    fp.seek(0)
    if writeLine in fp.read():
        print("Did not write move of " + comeFrom.decode("utf-8") + " as it was already there. Still attempting file move.")
        return False
    fp.write(writeLine)
    
# Read the moves.txt file, and move every file in the extracted dir to the base dir.
def reverseChanges(movesFile):
    try:
        fp = open(movesFile,"rb")
    except:
        print("Either moves file doesn't exist or wrong path given. Ensure path includes file name and ext.")
        return False
    moves = []
    # Remove all trailing spaces if there are any, shouldn't be but in case it was edited manually
    # Add every line (moved from, move to) to our list. Each read also moves the position we are at, and after reading all,
    # Position will be back at the end where it started when we opened the file for append
    # Since every line is a path in the order From, To, From, To, etc., create a list of pairs. We are guaranteed to have even number of items
    # Possibly make them from and to pairs of tuples?
    for line in fp:
        moves.append(line.strip())
    print("Retrieved all directories to move to and from. Now attempting all moves...")
    for i in range(0,len(moves),2):
        # Use extracted path as the one we come from, and the base path as the one we go to.
        fileFrom = os.path.normpath(moves[i+1].decode("utf-8"))
        fileTo = os.path.normpath(moves[i].decode("utf-8"))
        try:
            os.rename(fileFrom,fileTo)
            # continue
        except:
            print("Will not move " + fileFrom + " to " + fileTo)
    fp.close()

def main(base,extractTo):
    # Normalize paths
    newBase = os.path.normpath(base)
    newExtractTo = os.path.normpath(extractTo)
    # extensions we will look for
    exts = ["ogg","mp3","m4a","aac","mp4"]
    if not checkDirectories(newBase,newExtractTo):
        print("Both directories do not exist or path is not in correct form.")
        return False
    print("Both directories exist. Making list of moves in extract directory folder if file doesn't exist.")
    # If we can't open the moves list file, return False
    try:
        fp = open(createMoves(newExtractTo),"+ba")
    except:
        print("An error occured when trying to open the moves.txt file.")
        return False
    print("Moving all files from base and subdirectories into extract directory.")
    tuples = os.walk(newBase)
    for i,j,k in tuples:
        # If we have a files list in the current directory we are in, check it's extension against allowed extensions and move to extractTo dir
        # Also write where it came from and where it went in the list of moves file
        if k:
            for file in k:
                # index of last . from the right (so 3 letter extension would give us 3)
                ext = file[::-1].index(".")
                # all letters after last . (the exentsion of the file)
                # -index of last . gets us to last ., exclusive (so .txt would give us txt)
                ext = file[-ext:]
                if ext in exts:
                    # start getting file to extracted folder
                    # note we can't reverse, need to store comingFrom and goingTo renames so we can reverse
                    # If the entry doesn't exist, store it in some txt file?
                    fileFrom = os.path.join(i,file).encode("utf-8")
                    fileTo = os.path.join(newExtractTo,file).encode("utf-8")
                    
                    try:
                        writeMove(fp,fileFrom,fileTo)
                        os.rename(fileFrom.decode("utf-8"),fileTo.decode("utf-8"))
                        continue
                    except:
                        print("Either the moving info wasn't written, or the file failed to move. Will not move " + fileFrom.decode("utf-8") + " to " + fileTo.decode("utf-8"))
    fp.close()
                    
# main(basePath,extractPath)
# reverseChanges(movestxtPath)