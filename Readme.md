Cleaning up your calibre directories
=

Warning
= 
This script will *delete* folders from your system if matching criteria. These deletions cannot be undone and I am in no way responsible for important folders being deleted. 
Back up your folder first and review the python scripts for anything that does something that you do not want or expect. 


The script
-
It is python script that does the following things:
* From the given base folder it transverse all directories till it finds the leaf folders (subfolders without other folders)
* It checks if one of the file extensions is present that calibre supports.
* If none of these file extensions are there, the directory is marked for deletion
* At the end a list is given of all directories that are to be deleted.
* When instructed it will delete the list. 

Use
-
```text
USAGE:
Call by python CalibreCleaner.py <base_dir> <delete>
Params: base_dir [Optional] string: base directory of calibre library. Defaults to "/extra/calibre" 
        delete  [Optional] bool : True will delete the pegged directories, False will not. Defaults to False  
``` 
The script will not accept deletion of base paths shorter than 4 chars but you are still recommended not to pass a root dir. I do not have to explain that would be a bad idea now do I?
