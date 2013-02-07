#!/usr/bin/env python
"""Naval Fate.

Usage:
   mygits.py init
   mygits.py list
   mygits.py list [--repo_list]
   mygits.py add <url>
   mygits.py clean
   mygits.py pull
   mygits.py pull <name>
   mygits.py (-h | --help)
   mygits.py --version
   

Options:
  -h --help     Show this screen.
  --version     Show version.
  --all 

"""

from docopt import docopt
from os.path import expanduser, join , basename, exists
from os import makedirs, remove
import logging
from sh import git
from urlparse import urlparse

def setup_logging(name=None, console_level=logging.DEBUG):
    
    if name is None:
        name = basename(__file__)
    
    logger = logging.getLogger(name)
    logger.setLevel(console_level)
    ch = logging.StreamHandler()
    ch.setLevel(console_level)
    fmt =  '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(fmt)
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    
    if (console_level == logging.DEBUG):
        logger.debug("Starting debug for {}".format(name))
    return logger

def get_mygits_home():
    
    home = expanduser("~")
    mygits_dir = ".mygits"
    mygits_path = join(home, mygits_dir)
    
    return mygits_path
       
def add_repo(repo_url):
    
    mygits_path = get_mygits_home()
    
    repo_list_file = join(mygits_path, ".repo_list")
    
    logger.info("Adding {}".format(repo_url))
    repo_entries = []
    
    try:
        
        with open(repo_list_file, "r") as f:
            repo_entries = f.readlines()
    except IOError as e:
        if e.errno == 2:
            mygits_path = get_mygits_home()
            
            
        else:
            raise IOError(e)
        

    if repo_url in repo_entries:
        logger.warn("{} already added.".format(repo_url))
    else:
        repo_entries.append(repo_url)
    
    with open(repo_list_file, "w+") as f:
        for i in repo_entries:
            f.write(i+"\n")

def clean():
    my_gits_path = get_mygits_home()
    remove(join(my_gits_path, ".repo_list"))
    
    
def initialize():
    mygits_path = get_mygits_home()
    
    if not exists(mygits_path):
        msg =  """{} does not exist. Creating it.""".format(mygits_path)
        logger.info(msg)
        makedirs(mygits_path)
    else:
        msg =  "{} already exists. No need to create it."
        msg = msg + " Use 'init --force' to  really delete and recreate it"
        msg = msg.format(mygits_path)
        logger.info(msg)
        
def list(repo_list=False):
    mygits_home = get_mygits_home()
    repo_list_path = join(mygits_home, ".repo_list")
    
    if repo_list:
        with open (repo_list_path) as f:
            l = f.read()
            print l
            
def __clone_from_url(repo):
    
    urlpcs = urlparse(repo)
    
    if (urlpcs.scheme == '') and (urlpcs.netloc == ''):    
        raise ValueError("Cloning from a non http/https resource.")

    repo_name = basename(urlpcs.path)
    
    if urlpcs.path == "":
        raise ValueError("Invalid Repo URL {}".format(repo))
    
    
    mygits_home = get_mygits_home()    
    repo_path = join(mygits_home, repo_name)
    
    git("clone", repo, repo_path)
    
    
    
if __name__ == '__main__':
    logger = setup_logging()
    arguments = docopt(__doc__, version='mygits V 0.1')
    print(arguments)
    
    if arguments["init"] :
        initialize()
    
    if arguments["add"]:
        add_repo(arguments["<url>"])
        
    if arguments["clean"]:
        clean()
        
    if arguments["list"]:
        list(repo_list = arguments["--repo_list"])
        
    #repo =  "https://github.com/jnvilo/scripts"
    #__clone_from_url(repo)
        
        
        
    