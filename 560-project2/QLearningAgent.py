# import State, actions?
import sys, random
class QLearningAgent():
	def __init__(self, states):
		self.states = states
		# {{}} Q is action value of doing action a in state s
		self.Q = {}
		# {{}} N is the amount of times that each action is taken in each state
		self.N = {}
		# {{}} R = total reward earned by this state-action pair. 
		# reward = R[s][a] / N[s][a] 
		self.R = {}

		# checkSum value to know when Q values have stopped changing a lot
		self.checksum = 0.0
		
		# amount of iterations before checkSumLearning
		self.learning_iter = 100000

		# initialize Q, N, and U tables to zeroes across the board.
		for s in states:
			for a in states[s].actions:
				if s not in self.Q:
					self.Q[s] = {}
					self.N[s] = {}
					self.R[s] = {}
				self.Q[s][a] = 0.0
				self.N[s][a] = 0.0
				avail = len(list(self.states[s].actions.keys()))
				self.R[s][a] = 1.0 / avail
		#print(self.R)
		# discount factor models the ract that future rewards are worth less than immediate rewards
		self.discount_factor = 0.5
		# alpha is the learning rate - high = Q values often updated. low = Q values rarely updated
		self.alpha = 0.5

		# could be determined by still_learning function
		self.exploration_number = 1000

# TO DO: getPolicy, printQ
	def getTotalStateReward(self, state):
		reward = 0.0
		for action in self.states[state].actions:
			reward += self.R[state][action]
		return reward
	
	def getTotalStateNumber(self, state):
		number = 0.0
		for action in self.states[state].actions:
			number += self.N[state][action]
		return number

	def getAverageReward(self, state):
		if self.getTotalStateNumber(state) == 0:
			return 0
		return self.getTotalStateReward(state) / self.getTotalStateNumber(state)

	def updatePreviousReward(self, current_state, previous_state, action_taken):
		# reward of getting ball in hole is 1. Consider just putting this in the 'update reward' function
		# if TERMINAL(s) then Q[s, None] = r'. 
		if current_state == "In":
			add_reward = 1.0
		else:
			# get average reward total of R[s][a]. N[s][a] is incremented elsewhere
			add_reward = self.getTotalStateReward(current_state)
		if add_reward != 0:
			self.R[previous_state][action_taken] += (1.0 / add_reward)

		return None

	# get Max Q value calced first. then do f(calced, n[s][q]) as seen in the textbook.
	#tiebreaker is whichever is last
	def explore(self, state):
		if len(self.states[state].actions) is 1:
			return list(self.states[state].actions.keys())[0]

		first_action = list(self.states[state].actions.keys())[0]
		q_action = first_action
		r_action = first_action
		highest_Q = self.Q[state][first_action]
		for a in self.states[state].actions:
			if self.Q[state][a] >= highest_Q:
				highest_Q = self.Q[state][a]
				q_action = a

		# q_action = highest Q value OR the last one
		# highest_Q = that number.
		explore_N = self.N[state][q_action]

		if explore_N > self.exploration_number:
			return q_action
		else:
			# this is not correct. THis should have teh effect of trying each action-pair N times. 
			# return action choice with best theoretical reward (R+).
			# if the action with the highest Q value also has the highest reward, return the one with 2nd highest reward
			highest_reward = 0
			for a in self.states[state].actions:
				if self.N[state][a] != 0.0:
					if self.R[state][a]/self.N[state][a] >= highest_reward:
						if a != q_action:
							highest_reward = self.R[state][a]/self.N[state][a]
							r_action = a
			return r_action
			
			

	def QLearningAlg(self, current_state, previous_action, previous_state):

		if previous_state is not None:
			highest_Q = 0
			# ties broken by last
			for a in self.states[current_state].actions:
				if self.Q[current_state][a] >= highest_Q:
					highest_Q = self.Q[current_state][a]
			self.N[previous_state][previous_action] += 1
			self.Q[previous_state][previous_action] = self.Q[previous_state][previous_action] + \
				self.alpha*self.N[previous_state][previous_action] * ((self.R[previous_state][previous_action]/self.N[previous_state][previous_action]) + \
					self.discount_factor * highest_Q - self.Q[previous_state][previous_action])


			# explore (highest Q value of available actions in current state, number of times that action has been taken)
		return self.explore(current_state)

	# input: action, state
	# output: new state based on the input probabilities
	def takeAction(self,current_state, action_taken):
		
		# get a random probability
		probability_list = self.states[current_state].actions[action_taken].probabilities
		random_probability = random.randint(1,100)

		# an outcome happens based on the probabilities of action A in state S
		ctr = 0
		traverser = 0
		for i in probability_list:
			traverser += i
			if traverser >= random_probability:
				break
			ctr += 1

		new_state = self.states[current_state].actions[action_taken].outcomes[ctr]
		return new_state

	# calculate Utility policy based on Q values. U = maxa(Q(s,a))
	# ties by last
	def getPolicy(self):
		# {state: action_to_take}
		# action to take calculated by max(Qstate)
		utility_values = {}
		for s in self.states:
			max_q = self.Q[s][list(self.states[s].actions.keys())[0]]
			for a in self.states[s].actions:
				if self.Q[s][a] >= max_q:
					utility_values[s] = a

		return utility_values

	def checkSumLearning(self):
		q_sum = 0
		for s in self.states:
			for a in self.states[s].actions:
				q_sum += self.Q[s][a]
		diff = abs(q_sum - self.checksum) / learning_iter
		if diff < 1:
			return False
		else:
			return True


	def runQAnalysis(self):
		current_state = "Fairway"
		previous_state = None
		previous_action = None
		action_taken = None
		learning = True
		iterations = 0
		while learning:
			action_taken = self.QLearningAlg(current_state, action_taken, previous_state)
			# calculate what happens based on action based on given probabilities
			# update current_state, keep previous state saved
			previous_state = current_state
			current_state = self.takeAction(current_state, action_taken)

			# update previous reward to factor in the current state reached
			self.updatePreviousReward(current_state, previous_state, action_taken)

			# if current ball get in hole, put it on the fairway again and reset the values used in the Q algorithm.
			if current_state == "In":
				# handle the Q and N value of the action-state pair that gets the ball in the hole. 
				highest_Q = 1
				# ties broken by last
				#for a in self.states[current_state].actions:
				#	if self.Q[current_state][a] >= highest_Q:
				#		highest_Q = self.Q[current_state][a]
				self.N[previous_state][action_taken] += 1
				self.alpha = 1.0 / (self.N[previous_state][action_taken]) 
				self.Q[previous_state][action_taken] = self.Q[previous_state][action_taken] + self.alpha*self.N[previous_state][action_taken]\
					 * ((self.R[previous_state][action_taken]/self.N[previous_state][action_taken]) + self.discount_factor * highest_Q - \
						 self.Q[previous_state][action_taken])

				current_state = "Fairway"
				action_taken = None
				previous_state = None

			# every learning_iter iterations:
			# learning = checkSumLearning(self)
			iterations += 1
			if iterations > 1000000:
				learning = False
		print(self.N)
		return self.getPolicy()



		# Here's the deal. I need to do PolicySearch. But, this needs to be improved so that it matches the book - 
		# have to implement "if TERMINAL then Q[s, none] <- r'. your current way does NOT work. "
		# I need to OVERHAUL the way that I handle rewards