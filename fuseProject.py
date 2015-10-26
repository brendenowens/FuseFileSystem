'''Assignment 3 Fuse Filesystem
   Brenden Owens
   Ian Gaskill
   Jeremie Adams
   Tony Grace
   Pierce Albert
   CSCI-C435 Spring 2015
'''
#!/usr/bin/env python   
import errno  
import fuse    
import os,sys,glob
import subprocess as sp

#make dictonary 
open_files={}
#set the api version of fuse we want to use
fuse.fuse_python_api = (0, 2)  

class MyFS(fuse.Fuse):  

    #initialize the file system	
    def __init__(self, *args, **kw):  
	for x in sys.argv:
		print "***"+x
	print ":::::"+sys.argv[-2]
        fuse.Fuse.__init__(self, *args, **kw)
	
    #get the attributes of the file
    def getattr(self, path):  

	print "getattr-path: ",path
        return os.stat(sys.argv[-2]+path)

    #get the directory path of the file
    def readdir(self,path,offset):
	print "*** READDIR: ",path

	yield fuse.Direntry('.')
	yield fuse.Direntry('..')
	print ":::::"+sys.argv[-2]
	for x in os.listdir(sys.argv[-2]+path):
		yield fuse.Direntry(os.path.basename(x))

	return 
	
	
    #open the file and put it in the dictionary
    def open(self,path,flags):

	print "********* OPEN: ",path

	access_flags = os.O_RDONLY | os.O_WRONLY
	access_flags = flags & access_flags

        #find if the file should only be read
	if access_flags == os.O_RDONLY:
		fi=os.open(sys.argv[-2]+path,os.O_RDONLY)
		open_files[path]=fi
		print "fi "+str(fi)
		return 0

        #else it will be opened for writing
	else: 			
		fi=os.open(sys.argv[-2]+path, os.O_WRONLY)
		open_files[path]=fi
		print "fi "+str(fi)
		return 0

	return -errno.EACCESS

    #create the file if it wasn't found in the filesystem and open it for writing
    def create(self, path, flags):

	print "****CREATE: ",path
	fi=os.open(sys.argv[-2]+path,os.O_WRONLY)
        open_files[path]=fi
        return 0

    #read from the file
    def read(self,path,size,offset):

	print "****READ********: ",path,size,offset
	#open file
	fi=open_files[path]
	if fi != None:
            self.open(path,os.O_RDONLY)
            fi=open_files[path]
	#read our file
	return os.read(fi,size)

    #write to the file the user wants
    def write(self, path, buff, offset):

	print "***WRITE: ",path,offset	
	if path in open_files:
		fo=open_files[path]
		avg = os.open("countsPerMin.txt", os.O_RDONLY)
		count = os.read(avg, 15)
		os.close(avg)
		return os.write(fo,count)
		
	else:
		self.create(path, os.O_WRONLY)
		fo=open_files[path]
		avg = os.open("countsPerMin.txt", os.O_RDONLY)
		count = os.read(avg, 15)
		os.close(avg)
		return os.write(fo,count)
		
    #flush what ever is in the buffer 
    def flush(self, path, fh=None):

	print "***FLUSH: ",path

	if path in open_files:
		fh=open_files[path]
		os.fsync(fh)

	return 0

    #close the file since we are done with it
    def release(self, path, fh=None):

	print "***RELEASE: ",path
	os.close(fh)
	del open_files[path]

	return 0

    #unlink the file, or more commonly delete
    def unlink(self, path):
	
	print "***UNLINK: ",path

	if path in open_files:
		return -errno.ENOSYS

	os.unlink(sys.argv[-2]+path)
	return 0
	
    #rename the file with a new path
    def rename(self, oldpath, newpath):

	os.rename(sys.argv[-2]+oldpath,sys.argv[-2]+newpath)
	return 0
         


 
if __name__ == '__main__': 
    #start our raspberry code running in the backround 
    rasp = sp.Popen(['python', './raspberry.py' , '&'])
    #create an instance of the fuse class
    fs = MyFS()  
    fs.parse(errex=1) 
    #start the fuse filesystem    
    fs.main() 
    #fuse has been unmounted and we are done with the raspberry pi
    #kill the raspberry pi program
    rasp.kill()
    #remove the binary.bin file
    sp.call(['rm','./binary.bin'])
    #remove the countsPerMin.txt file
    sp.call(['rm','./countsPerMin.txt'])
