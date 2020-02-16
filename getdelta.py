#!/usr/bin/python3
#
# Script takes 2 files (old and new) with unsorted lines
# and creates 2 new files in current working directory:
#   delta_remove.txt  - lines from "old" that not present in "new"
#   delta_append.txt - lines from "new" that not present in "old"
# Empty lines will be ignored
#

import sys
from hashlib import md5


def main():

    if len(sys.argv) != 3:
        print("Usage:")
        print(sys.argv[0], "fileOld fileNew")
        print("Will create 2 files: delta_remove.txt and delta_append.txt")
        exit(-2)

    file_old = sys.argv[1]
    file_new = sys.argv[2]
    target_path_remove = 'delta_remove.txt'
    target_path_append = 'delta_append.txt'

    # old and new files have the same path
    if file_old == file_new:
        with open(target_path_remove, 'w') as rm_fp:
            with open(target_path_append, 'w') as append_fp:
                # create empty delta files and exit
                exit(0)
    else:
        with open(target_path_remove, 'w') as rm_fp:
            with open(target_path_append, 'w') as append_fp:
                try:
                    with open(file_new, 'r') as new_fp:
                        with open(file_old, 'r') as old_fp:
                            write_new_strings_for_large_files(new_fp, old_fp, append_fp)
                            write_new_strings_for_large_files(old_fp, new_fp, rm_fp)
                            exit(0)
                except OSError as err:
                    print("%s:" % err.strerror, err.filename)

    print("Fatal error.")
    exit(-1)


def hash_func(line):
    encoding = 'utf-8'
    return md5(line.encode(encoding)).hexdigest()[:16]


'''
Read files from file-pointers and write into out_fp
lines from the 1st file that are not in the 2nd file.
There are 2 solutions:
'''


def write_new_strings(file1_fp, file2_fp, out_fp):
    """
    Solution 1 - for small files
    """
    file1_fp.seek(0)
    for line1 in file1_fp:
        file2_fp.seek(0)
        line1_found = False
        line1 = line1.rstrip("\r\n")
        if not line1:
            continue
        for line2 in file2_fp:
            if line1 == line2.rstrip("\r\n"):
                line1_found = True
                break
        if not line1_found:
            out_fp.write(line1 + "\n")


def write_new_strings_for_large_files(file1_fp, file2_fp, out_fp):
    """
    Solution 2 - for Large files (100+ GB) with long lines
    """

    # store hashes of 2nd file's lines into memory
    second_file_hashes = {}
    file2_fp.seek(0)
    line2 = file2_fp.readline()
    while line2:
        line2 = line2.rstrip("\r\n")
        if line2:
            second_file_hashes[hash_func(line2)] = None
        line2 = file2_fp.readline()

    print("..Finished to read file")

    # read 1st file and check for hash coincidence
    file1_fp.seek(0)
    for line1 in file1_fp:
        line_no_eol = line1.rstrip("\r\n")
        if line_no_eol:
            digest = hash_func(line_no_eol)
            if digest not in second_file_hashes:
                out_fp.write(line_no_eol + "\n")

    print("..Finished to read file")


if __name__ == '__main__':
    main()
