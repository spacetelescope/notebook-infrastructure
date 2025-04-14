import os
import re

# TO-DO: get notebook titles
# from nbtitle import read_title

class Notebook():
    ''' Notebooks may be in a topic or in a chapter
    '''
    def __init__(self, root, name):
        self.root = root
        # name should really be extracted from the title of the NB
        self.name = name
        self.path = os.path.join(root, name)

        all_files = os.listdir(self.path)
        # ignore checkpoint files
        f = re.compile(r".*(?<!-checkpoint)\.ipynb$")

        nb_file = list(filter(f.match, all_files))

        # mast_notebooks has a double-nb folder: need to fix
        if len(nb_file) == 1:
            self.nb_file = os.path.join(self.path, nb_file[0])
        else:
            self.nb_file = ""

        # TO-DO: fully implement reading titles
        #self.title = read_title(self.path)


class Topic():
    ''' Topics may be in a chapter, or they may be a "sub-topic"
    '''
    def __init__(self, root, name):
        # the root is the "directory path so far"
        self.root = root
        self.name = name
        
        # path to the topic
        self.path = os.path.join(root, name)
        
        # prepare an empty list to hold notebooks
        self.nbs = []
        
        # get all directories, then...
        all_dirs = os.listdir(self.path)
        # filter out any .checkpoints or other weird files
        r = re.compile(r"[^\.]")
        clean_dirs = list(filter(r.match, all_dirs))
        # and finally, make sure we only include directories
        dirs_only = list(filter(os.path.isdir,  [os.path.join(self.path, d) for d in clean_dirs]))

        # go thru directories -- since this is the full path, just keep the last part
        for d in dirs_only:
            d = d.split("/")[-1]
            self.nbs.append(Notebook(self.path, d))
            
        # look for markdown files but exclude checkpoints
        g = re.compile(r".*(?<!-checkpoint)\.md$")
        md_file = list(filter(g.match, all_dirs))[0]
        if md_file:
            self.md_path = os.path.join(self.path, md_file)
        

class Chapter():       
    '''A chapter may contain topic directories OR notebook directories.
    It should not contain any bare notebooks
    '''
    def get_dirs_files(self):
        # get all dirs, then clean with regex
        r = re.compile(r"[^\.]")
        all_dirs = os.listdir(self.path)
        clean_dirs = list(filter(r.match, all_dirs))
        return clean_dirs

    def __init__(self, root, name):
        # the root is the "directory path so far"
        self.root = root
        self.name = name 
        self.path = os.path.join(root, name)

        # list of files AND dirs within the chapter dir
        # (note: should only be dirs at this level)
        self.files = self.get_dirs_files()
        self.topics = []
        self.nbs = []

        # loop through all of the directories
        for file in self.files:
            # get the path
            fp = os.path.join(self.path, file)
            if os.path.isdir(fp):
                # get all of the subfiles
                sub_files = os.listdir(fp)
                # if there is a markdown file, then this is a topic folder
                if any([re.search(r"(?<!-checkpoint)\.md$", file) for file in sub_files]):
                    self.topics.append(Topic(self.path, file))
                # if there is an ipynb file, this is a notebook folder
                if any([re.search(r"(?<!-checkpoint)\.ipynb$", file) for file in sub_files]):
                    self.nbs.append(Notebook(self.path, file))


class Book():
    def get_clean_dirs(self):
        # regex match for .DS_Store and .checkpoints
        r = re.compile(r"[^\.]")
        # get all entries in this directory
        all_files = os.listdir(self.path)
        # keep only matching regex entries
        clean_files = list(filter(r.match, all_files))
        return clean_files
    
    def __init__(self, path):
        self.path = path
        self.chapter_names = self.get_clean_dirs()
        self.chapters = []

        print(self.chapter_names.sort(key=lambda c: c.lower()))
        for chpt in self.chapter_names:
            self.chapters.append(Chapter(self.path, chpt))