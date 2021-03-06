<<<<<<< HEAD
import zipfile
=======
#!/usr/bin/env python

>>>>>>> 080c4626550cdb11fe2bc078b655fc117fb66ddd
from urlparse import urlparse
import os
from shutil import rmtree
import subprocess
import zipfile
from import_or_pip import import_or_pip

requests = import_or_pip("requests")


from os.path import expanduser

class InstallFromGithub(object):
    
    def __init__(self, username=None, password=None, repo=None):
        
        self.url = "https://github.com/" + username + "repo/archive/master.zip"
        
        
        

class DjangoInstaller(object):

    def __init__(self):

        self.url =  "https://github.com/jnvilo/django/archive/master.zip"
        self.filename = self.__filename_from_url(self.url)
        self.src_dir = self.__get_src_dir()
        self.path = os.path.join (self.src_dir, self.filename)
        self.extracted_path =  os.path.join(self.src_dir, "django-master")

        self.__download(self.url, self.path, force=False)
        self.unzip()
        self.install()

    def __download(self, url, path, force=False):

        if (force == False) and (os.path.exists(path)):
            print "Already downloaded..."
            return False
        else:
            #Force a redownload
            print "Already downloaded but we are forced to get it again"
            download = requests.get(url)

            with open(path, "w") as f:

                f.write(download.content)
                print "wrote: {}".format(path)
            return True

    def __get_src_dir(self):
        home = expanduser("~")
        src_dir = os.path.join(home, "src")


        if os.path.isdir(src_dir) == False:
            os.makedirs(src_dir)

        return src_dir


    def __filename_from_url(self, url):

        u = urlparse(url)
        path = u.path
        filename = os.path.basename(path)
        return filename


    def unzip(self):

        path = self.path
        src_dir = self.src_dir

        extracted_path = self.extracted_path 
        if os.path.exists(extracted_path):
            import shutil
            print "{} already exists. Removing it".format(src_dir)
            shutil.rmtree(extracted_path)


        x = zipfile.ZipFile(path)
        x.extractall(src_dir)


    def install(self):

        import subprocess
        import sys
        
        #are we running in a VIRTUALENV?
        try:
            virtualenv_path = os.environ["VIRTUALENV"]
            python_bin = os.path.join(virtualenv_path, "bin/python")
            
        except KeyError as e:
            #if we get here then VIRTUALENV is not set.
            python_bin = "python"
        
        cmd = [python_bin,
               "{}/setup.py".format(self.extracted_path), "install"]
        print "executing: {}".format(cmd)
        process = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )

        while True:
            out = process.stdout.read(1)
            if out == '' and process.poll() != None:
                break
            if out != '':
                sys.stdout.write(out)
                sys.stdout.flush()      


if __name__ == "__main__":

    x = DjangoInstaller()

