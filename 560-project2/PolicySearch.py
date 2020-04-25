class PolicySearch():
	def __init__(self, states):
		self.states = states
		# u is an index of expected value for taking action a in state s
		self.U = {}
		self.policy = {}
		for s in states:
			for a in states[s].actions:
				if s not in self.Q:
					self.Q[s] = {}
				self.Q[s][a] = 0
				self.U[s] = 0

	# play golf and update the hits + taken for each of the actions
	# choose actions sometimes based on exploration or exploitation. use explore_exploit maybe to determine which to do - explore or exploit

	def playGolf(self, explore_exploit):

		return None


	# update utility function based on any changes (run after PLAY GOLF)
	def updateUtility(self):

		return None

	# policy: {state: index of preferred action}
	# U: {state: {action: utility}}
	# compared utility of action, see which is lowest. Policy should be the lowest one. 
	# IS POLICY STOCHASTIC?????? - 'TRANSITION PROBABILITIES FOR EACH STATE???'
	def evalPolicy(self):
		for state in self.states:
			highest = 0
			for action in state.actions:
				# compare utility of action to policy - make sure they match. if not, change. 
		return None
	

	def searchForPolicy(self):
		while(True):
			
			condition = False
			if condition:
				break
			# exit condition - utilities don't get updated much, but by how much?


