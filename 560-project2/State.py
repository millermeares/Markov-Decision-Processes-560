class State:
	def __init__(self, name): 
		# keep a running tally of average total score per iteration per action. At some point, update this value for each state so that the state gains a preference. 
		# need some sort of evaluation function? Somehow, that needs to make its way here. 
		self.name = name
		self.actions = {}