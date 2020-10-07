import random 


class threads():
	#constructor
	def __init__(self):
		print ("This is the constructor")
		
		for i in range(5):
			x = random.randint(0,100)
			print (x)


newobj = threads()
