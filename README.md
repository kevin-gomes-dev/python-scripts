Random python scripts I made to help with very specific cases of mine. Figure I dump them here in the event someone could use them or just to save for future use. Note that some of these modify files on your system. Please take care, and do not use if you do not trust (since all code is publicly available, you can decide if it's safe). I also didn't really handle error checking too much. Not the main concern.

# extractor
Extract all files from a directory/subs into another directory, and allows reversal via created moves.txt file, containing all the path pairs of base + extracted. Note this does not keep the subdirectory setup, so only raw files will be moved with all directories left intact (just emptying them). Reversing changes however respects the subdirectories and moves them back to exactly where they were. It does (should) support all forms of paths, so OS is irrelevant. Run using your preferred python version like so:

If I want to extract all items and subdirectory structure from dir A to dir B:  
python extractor.py extract "C:/Users/JohnnyRocketfingers/Desktop/SecretStash/dirA" "C:/Users/JohnnyRocketfingers/Desktop/SecretStash/dirB"

If I want to reverse changes (by default we save our moves to the extracted dir):  
python extractor.py reverse "C:\Users\JohnnyRocketfingeres\Desktop\SecretStash\dirB\moves.txt"

# renaming
Prefixes filenames in a directory/subs with given string. If using different mode, finds wherever the string is in the filename and removes.

# update_m4a
Takes a directory and updates every file to be a version where the 'title' tag is changed to the filename. Very little error checking is here. It could be updated to do whatever extensions you want I guess. 
