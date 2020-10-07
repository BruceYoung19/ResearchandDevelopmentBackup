import random 
import threading

class objs():
	
	#constructor
	def __init__(self):
		print ("This is the constructor")
		x = random.randint(0,100)
		self.object = x
		print (self.object)

# class for 
class threads():
	
	def chain():
		k = objs()
		x = threading.Thread(target=k,args=(1,))
		#x.start()
			
	
	def run():
		for i in range(5):
			td = threads.chain()
			print("run has started")
			
if __name__ == "__main__":
	print("main started")
	threads.run()