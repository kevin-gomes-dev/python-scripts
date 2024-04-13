# Cross platform and handles unique utf-8 filenames. For duplicate names, adds a (count) to the end where count is 1 or 2 or 3...
# Extract all files of a certain type from the path given as well as all subdirectories. They are extracted at the other path given.
# All original paths are put in a file to be able to undo this and restore their paths. The subdirectories will not be deleted.
# That way we can keep moving stuff and have a running list of all the moves to reverse more than once
# Use bytes instead of strings for utf-8 encoding (many artists not in English, special characters in song names, etc.)
# TODO: Add either text interface for options, changing exts, reverse/move, etc. OR create a gui with buttons for this. See QtWidget?

# Created by Kevin Gomes

import os
import sys

def fixPath(path):
    return os.path.normpath(os.path.realpath(path))

def checkDirectories(baseDir = "",extractToDir = ""):
    if baseDir == extractToDir:
        return False
    if not (os.path.isdir(baseDir) and os.path.isdir(extractToDir)):
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
        print("Will attempt file move, but did not write move of " + comeFrom.decode("utf-8") + " as it was already there.")
        return False
    fp.write(writeLine)
    
# Check arguments length and values. Returns true if valid, false otherwise
def checkArgs():
    args = sys.argv
    # at least 2 args
    if len(args) < 3:
        print("Did not pass correct amount of arguments.")
        return False
    mode = args[1]
    
    # mode incorrect
    if mode != "extract" and mode != "reverse":
        print("Mode: " + mode)
        print("Mode expected to be either 'extract' or 'reverse'")
        return False
    
    if mode == "extract":
        # mode was extract, but not enough args
        if len(args) != 4:
            print("When extracting, expected 2 directories. One base, one to extract to.")
            return False
    
        # dirs not legal in extract
        path1 = fixPath(args[2])
        path2 = fixPath(args[3])
        print("Extract base: " + path1)
        print("Extracting to: " + path2)
        if not checkDirectories(path1,path2):
            print("One or both directories don't exist or are the same. Use quotation marks around paths to avoid OS specific ambiguity.")
            return False
        
    # dir and reversal txt file are not supplied
    if mode == "reverse":
        movesFile = fixPath(args[2])
        if not os.path.isfile(movesFile):
            print("Didn't supply a reversal txt (most likely moves.txt)")
            return False
    return True

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
    # Possibly make them from and to pairs of tuples? Or [[from,to],[from,to]]?
    for line in fp:
        moves.append(line.strip())
    print("Retrieved all directories to reverse moves. Now attempting all moves.")
    print()
    for i in range(0,len(moves),2):
        # Use extracted path as the one we come from, and the base path as the one we go to.
        fileFrom = fixPath(moves[i+1].decode("utf-8"))
        fileTo = fixPath(moves[i].decode("utf-8"))
        try:
            os.rename(fileFrom,fileTo)
        except:
            print("Will not reverse " + fileFrom + " to " + fileTo + ", perhaps file or path doesn't exist?")
    print("Done reversing moves!")
    fp.close()

def main():
    if not checkArgs():
        print("Something went wrong checking arguments. Check error message above. If none, create issue on github")
        return False
    mode = sys.argv[1]
    if mode == "reverse":
        reverseChanges(sys.argv[2])
        return True
    # Normalize paths
    base = fixPath(sys.argv[2])
    extractTo = fixPath(sys.argv[3])
    # extensions we will look for
    exts = [".ogg",".mp3",".m4a",".aac",".mp4"]
    if not checkDirectories(base,extractTo):
        print("Both directories do not exist or are exactly the same.")
        return False
    print("Both directories exist. Making list of moves in extract directory if file doesn't exist.")
    # If we can't open the moves list file, return False
    try:
        fp = open(createMoves(extractTo),"+ba")
    except:
        print("An error occured when trying to open the moves.txt file.")
        return False
    print("Moving all files from base and subdirectories into extract directory.")
    print()
    tuples = os.walk(base)
    for i,j,k in tuples:
        # If we have a files list in the current directory we are in, check it's extension against allowed extensions and move to extractTo dir
        # Also write where it came from and where it went in the list of moves file
        if k:
            for file in k:
                fileName,ext = os.path.splitext(file)
                if ext in exts:
                    # start getting file to extract directory
                    fileFrom = os.path.join(i,file)
                    fileTo = os.path.join(extractTo,file)
                    try:
                        # First check if file exists. If so, add something to make it unique. Copying windows naming of (1) (2) etc...
                        if os.path.exists(fileTo):
                            print(fileTo + " already exists. Will add number to ensure unique filename.")
                            count = 1
                            while True:
                                # Something like "sample (1).txt or sample (4).txt"
                                newFileName = fileName + " (" + str(count) + ")" + ext
                                fileTo = os.path.join(extractTo,newFileName)
                                if not os.path.exists(fileTo):
                                    print("Final name: " + newFileName)
                                    break
                                count += 1        
                        writeMove(fp,fileFrom.encode("utf-8"),fileTo.encode("utf-8"))
                        os.rename(fileFrom,fileTo)
                    except:
                        print("Either the moving info failed attempting write, or the file failed to move. Will not move " + fileFrom + " to " + fileTo)
    print("Done moving all files!")
    fp.close()

def test():
    checkArgs()

main()