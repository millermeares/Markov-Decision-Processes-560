class Actions:
	def __init__(self, action):
		self.action = action # string
		# two arrays instead of a library because of the random number calculatoin
		self.outcomes = [] # string
		self.probabilities = [] # integers because floats were causing problems