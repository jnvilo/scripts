from urlparse import urlparse
import os
from shutil import rmtree
import subprocess
import zipfile
from urlparse import urlparse

try:
    import requests
except ImportError as e:
    subprocess.check_call("pip install requests", shell=True)
    import requests
    
try:
    from pathlib import Path
except ImportError as e:
    subprocess.check_call("pip install pathlib", shell=True)
    from pathlib import Path
    

class PathError(Exception):
    
    def __init__(self, msg= None):
        if msg != None:
            self.message = msg
        else:
            self.message = "Path does not exist"

class PyGet(object):
    
    def __init__(self, url, filename = None, dest_dir = None):
        
        if dest_dir == None:
            self.dest_dir = os.getcwd()
        else:
            self.dest_dir = dest_dir
            
        if os.path.exists(self.dest_dir) == False:
            raise PathError("dest_dir does not exist")
        
        parse_result = urlparse(url)
        
        if filename == None:
            self.filename = os.path.basename(parse_result.path)
        else:
            self.filename = filename
            
        self.path = os.path.join(self.dest_dir, self.filename)
        
        self.url = url
        
        
    def get(self):
        
        r = requests.get(self.url, stream=True)
        size = int(r.headers['Content-Length'])
        self.bytes = 0
        
        print "Getting the file"
        
        with open(self.path, "w") as f:
            for buf in r.iter_content(1024):
                if buf:
                    print "Got 1024"
                    f.write(buf)
                    
                
                
if __name__ == "__main__":
    
    print "running"
    p = PyGet("http://box.j2code.com/media/101%20Running%20Songs%20Lap%202%205cds%202010%20+covers%20320@BSBT/CD1/4.%20Song%202%20-%20Blur.mp3",
              dest_dir="/Users/jasonviloria/")
    
    print p
    print p.filename
    print p.path
    
    p.get()
    
    print "Done"
    
    
    
        
        
        
            
        
        
            
        
            
        
        