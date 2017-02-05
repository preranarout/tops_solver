class Square:
	side = 0

	def __init__(self, side_):
		self.side = side_    # instance variable unique to each instance

	def area(self):
	    return self.side**2

	def perimeter(self):
		return self.side*4

	def __str__(self):
		return ("Side of square " + str(self.side))

def side_of_square(square):
	return square.side

print ("Hello world!")