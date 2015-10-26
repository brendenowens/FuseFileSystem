'''Assignment 3 Fuse Filesystem
   Brenden Owens
   Ian Gaskill
   Jeremie Adams
   Tony Grace
   Pierce Albert
   CSCI-C435 Spring 2015
'''
#!/usr/bin/ev python
import os,sys, subprocess as sp
#get user input
print "Enter the file you want to open: "
fi = raw_input("-->")
#open the asked for file
reading=os.open(fi, os.O_RDONLY)
#closing flag
closing = False
#run while the user wants
while not closing:
	print "How many bytes do you want to read: "
	bytes = raw_input("-->")
	# multiply the int we receive by 8 to convert to bits
	bytes = int(bytes)*8
	# call os read with our number of bytes and display results to user
	print os.read(reading,bytes)
	print "Do you want to write: (y/n)"
	ans = raw_input("-->")
	if ans == 'y':
		print "What file do you want to write to? "
		ans = raw_input("-->")
		# use os open to open appropriate file
		writing = os.open(ans, os.O_WRONLY)
		# use os write to write our counts, hello is passed as a dummy string
		# since the os write expects a string to be passed
		os.write(writing,'hello')
		# close our file
		os.close(writing)
		
	else:
		print 'not writing'
	print 'Do you want to exit: (y/n)'
	exit = raw_input('-->')
	if exit == 'y':
		# if user wants to exit set closing to true
		closing = True
		# close our file
   		os.close(reading)
                

