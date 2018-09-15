import os
import sys
import shutil
import time

"""
USAGE:
Call by python CalibreCleaner.py <base_dir> <delete>
Params: base_dir [Optional] string: base directory of calibre library. Defaults to "/extra/calibre" 
        delete  [Optional] bool : True will delete the pegged directories, False will not. Defaults to False  
"""

# List of all dirs to delete
collection_of_deletable_dirs = []

# List of all extensions to flag a directory not to be deleted.
collection_of_possible_formats = ["epub",
                                  "pdf",
                                  "lit",
                                  "txt",
                                  "mobi",
                                  "azw",
                                  "azw3",
                                  "azw4",
                                  "zip",
                                  "rar",
                                  "doc",
                                  "docx",
                                  "rtf",
                                  "cbr",
                                  "cbz",
                                  "cbc",
                                  "djvu",
                                  "prc",
                                  "chm",
                                  "fb2",
                                  "html",
                                  "ps",
                                  "mp3",
                                  "htmlz",
                                  "djvu",
                                  "djv",
                                  "odt",
                                  "rb",
                                  "tcr",
                                  "txtz"]

# List of extensions present in the directories to be deleted to check if there are any extensions missing from the set.
collection_of_extensions = []

# Default values  ######################################################################################################
base_path = "/extra/calibre"
delete_request = False
# ######################################################################################################################

# Process params  ######################################################################################################
if len(sys.argv) == 2:
    base_path = sys.argv[1]
if len(sys.argv) > 2:
    delete_request = bool(sys.argv[2])

'''
Scans the directories and added the matching containers to be deleted. 
Param  : source_dir
Returns: void      
'''


def collect_directories(source_dir):
    progress_ix = 0
    for root, subdirs, files in os.walk(source_dir):
        progress_ix += 1
        if (progress_ix % 1000) == 0:
            num_deletable = len(collection_of_deletable_dirs)
            percentage = (num_deletable / progress_ix) * 100
            print(
                "Processing number {}, deletable found: {}, percentage: {}".format(str(progress_ix), str(num_deletable),
                                                                                   str(percentage)))
        if len(subdirs) == 0 and len(files) != 0:
            # print("This is a leaf folder  : Root is {}, with files {}".format(root, files))
            has_ebooks = False
            for file in files:
                file_ext = file.split(".")[-1].lower()
                if file_ext in collection_of_possible_formats:
                    has_ebooks = True
                    break

            if not has_ebooks:
                # print(" --- folder {} can be deleted it contains no ebooks ".format(root))
                collection_of_deletable_dirs.append(root)
        # Get rid of empty folders at all.
        elif len(subdirs) == 0 and len(files) == 0:
            print("------ Empty folder {}".format(root))
            collection_of_deletable_dirs.append(root)


'''
Lists extensions that were in the directories to be deleted. 
Params  : None
Returns : void
'''


def what_extensions_do_the_rejects_have():
    ext_collection = []
    for dir in collection_of_deletable_dirs:
        for root, subdirs, files in os.walk(dir):
            for file in files:
                file_ext = file.split(".")[-1]
                if file_ext not in ext_collection:
                    ext_collection.append(file_ext)
    return ext_collection


'''
Do the actuele delete
Param: do_delete : True or False, defaults to False
Returns : void 
'''


def delete_folders(do_delete=False):
    for dir in collection_of_deletable_dirs:
        # Checks if there is no spurious root path delete instruction is passed here.
        if len(dir) > len(base_path) + 4:
            print("About to delete rm -rf {}".format(dir))
            if do_delete:
                shutil.rmtree(dir)


# ENTRYPOINT ###########################################################################################################
if __name__ == '__main__':
    tic = time.perf_counter()
    collect_directories(base_path)

    for delete_candidate in collection_of_deletable_dirs:
        print("  ---- {}".format(delete_candidate))
    print("List of deletable folders, {} found".format(str(len(collection_of_deletable_dirs))))
    exts = what_extensions_do_the_rejects_have()
    for ext in exts:
        print("  - Extension in rejects: {}".format(ext))
    delete_folders(delete_request)
    toc = time.process_time()
    print("Process took {} seconds systemtime ".format(str((tic - toc) / 1000)))
