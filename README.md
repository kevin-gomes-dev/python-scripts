# extractor
Small messy python script to extract all files from a directory/subs into another directory, and allows reversal via created moves.txt file, containing all the path pairs of base + extracted. Currently need to edit the .py to change paths, choose reversing or moving, and the exts you want. Changes to this should be done such that we either have a terminal interface for choosing these or a gui accessing some kind of config file. QtWidget + a config for saved extensions and paths would do nicely.
