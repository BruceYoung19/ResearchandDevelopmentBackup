import random 
import threading

class objs():
	
	#constructor
	def __init__(self, name):
		print ("This is the constructor")
		x = random.randint(0,100)
		self.object = x
		self.name = name
		print (self.object)

	def displayName(self):
		print "Total Employee %d" % objs.name


# class for threads
class threads():
	
	def chain():
		k = objs("jim")
		objs.displayName()
		x = threading.Thread(target=k,args=(1,))
		#x.start()

			
	
	def run():
		for i in range(5):
			td = threads.chain()
			print("run has started")

if __name__ == "__main__":
	print("main started")
	threads.run()
	print("Program has stopped")
	
