class Action:
	def __init__(self, action):
		self.action = action # string
		# two arrays instead of a library because of the random number calculatoin
		self.outcomes = [] # string
		self.probabilities = [] # integers because floats were causing problems
		# hits  = total amount of hits taken after an action is taken
		# taken = total times an action was taken
		self.hits = 0
		self.taken = 0
		self.reward = 0