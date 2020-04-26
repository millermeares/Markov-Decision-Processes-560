class Action:
	def __init__(self, action):
		self.action = action # string
		# two arrays instead of a library because of the random number calculatoin
		self.outcomes = [] # string
		self.probabilities = [] # integers because floats were causing problems
		# {outcome: number of times it occurred in model}
		self.num_outcomes = {}
		# {outcome: probability}
		self.new_prob = {}
		# total_remaining_hits
		self.shots_to_in = 0
		# actions_taken
		self.swings = 0
		# reward = total_remaining_hits / swings
		self.reward = 0
