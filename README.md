# extractor
Note that this modifies files on your system. Please take care, and do not use if you do not trust (since all code is publicly available, you can decide if it's safe).

Small messy python script to extract all files from a directory/subs into another directory, and allows reversal via created moves.txt file, containing all the path pairs of base + extracted. Note this does not keep the subdirectory setup, so only raw files will be moved with all directories left intact (just emptying them). Reversing changes however respects the subdirectories and moves them back to exactly where they were. It (should) supports all forms of paths, so OS is irrelevant. Run using your preferred python version like so:

If I want to extract all items and subdirectory structure from dir A to dir B:
python extractor.py extract "C:/Users/JohnnyRocketfingers/Desktop/SecretStash/dirA" "C:/Users/JohnnyRocketfingers/Desktop/SecretStash/dirB"

If I want to reverse changes (by default we save our moves to the extracted dir):
python extractor.py reverse "C:\Users\JohnnyRocketfingeres\Desktop\SecretStash\dirB\moves.txt"
