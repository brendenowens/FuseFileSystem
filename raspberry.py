'''Assignment 3 Fuse Filesystem
   Brenden Owens
   Ian Gaskill
   Jeremie Adams
   Tony Grace
   Pierce Albert
   CSCI-C435 Spring 2015
'''
#!/usr/bin/env python
import pigpio, time
class Rasp():
	#initialize our variables at 0
        def __init__(self):
            self.running_time = 0
            self.count = 0


        #gather events and populate array with random bits based on time differential
	def random_bits(self):
		#set up pi for gathering random bits
		pi = pigpio.pi()
		pi.set_mode(23, pigpio.INPUT)
		time.sleep(5)
		times = []
		timeDiff = []   
		#do forever
		while 1: 
			#get start time
			startTime = time.time() 
			#wait for event
			if pi.wait_for_edge(23, pigpio.FALLING_EDGE, 5.0):
					#increment count
					self.count += 1
					#get end time
					endTime = time.time()
					#put time differential in times array
					times.append(endTime - startTime)
					self.running_time = self.running_time + (endTime-startTime)
					#if we have enough times to compare we compare them					
					if len(times) == 2:
						#write difference to timeDiff
						timeDiff.append(times[1] - times[0])
						times=[]
						if len(timeDiff) == 2:
							#if time difference is smaller than previous write a 1
							if timeDiff[0] > timeDiff[1]:
								 bit = '1'
								 binary = open('binary.bin', 'ab')
								 binary.write(bit)
								 binary.flush()
								 counts = open('countsPerMin.txt', 'w')
								 counts.write(str((self.count / self.running_time)*60))
								 counts.flush()
								 counts.close()
								 binary.close()
								 timeDiff = []
								 times = []
							# if time difference is larger than previous write a 0
							elif (timeDiff[0] < timeDiff[1]):
								 bit = '0'
								 binary = open('binary.bin', 'ab')
								 binary.write(bit)
								 binary.flush()
								 counts = open('countsPerMin.txt', 'w')
								 counts.write(str((self.count / self.running_time)*60))
								 counts.flush()
								 counts.close()
								 binary.close()
								 timeDiff = []
								 times = []
							# if time difference is equal don't write
							else:
								
								 timeDiff = []
								 times = []

#main method create instance of rasp and start random bit gathering
def main():
	rasp = Rasp()
	rasp.random_bits()
#start main
if __name__ == '__main__':
	main()

