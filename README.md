# Delta2Files

Extract sort-independent line difference from 2 large files.

Script takes 2 files (old and new) with unsorted lines and creates 2 new files in current working directory:

  * delta_remove.txt  - lines from "old" that not present in "new"
  * delta_append.txt - lines from "new" that not present in "old"

Empty lines will be ignored.

# Purpose of this
Network transfer the difference between large text files (in which line order is not important).

# Why not *"git format-patch"*
Large files.
This script tested on files more than 120GB, 
on which *"git format-patch"* or *"git commit"* fails with fatal error on the machine with 32GB RAM. 
At the same time, my solution consumes about 2GB on the same files.

Note that, this script doesn't take line order into account.