# import State, actions?
import sys, random
class QLearningAgent():
	def __init__(self, states):
		self.states = states
		# {{}} Q is action value of doing action a in state s
		self.Q = {}
		# {{}} N is the amount of times that each action is taken in each state
		self.N = {}

		# checkSum value to know when Q values have stopped changing a lot
		self.checksum = 0.0
		self.checked = 1

		# alpha is the learning rate - high = Q values often updated. low = Q values rarely updated
		# if the value of alpha is too low, the system will not learn. The higher the value of alpha, the higher the value of epsilon needs to be
		self.alpha = 0.1
		self.epsilon = 0.00001

		#learning_iter is the amount of iterations before checksum checks. 
		self.learning_iter = 10000

		# discount factor models the ract that future rewards are worth less than immediate rewards
		self.discount_factor = 0.5

		# becaues the learning space is potentially infinite, big_N is the amount of iterations each action needs to have before the 
		# explore function starts to choose best Q value. As of now, it's arbitrary (0.2 * learning_iter)
		# idea: big_N = 1 / 2(len(states].actions)) * learning_iter
		self.big_N = 0.2

		# initialize Q, N, and U tables to zeroes across the board.
		for s in states:
			for a in states[s].actions:
				if s not in self.Q:
					self.Q[s] = {}
					self.N[s] = {}
				self.Q[s][a] = 0.0
				self.N[s][a] = 0.0
		self.iterations = 0


		# values for q
		self.previous_state = None
		self.previous_action = None
		self.previous_reward = None
		self.current_action = None
		self.current_state = "Fairway"
		self.current_reward = None

	
	def explore(self, state):
		if len(self.states[state].actions) is 1:
			return list(self.states[state].actions.keys())[0]

		for i in range(0,len(self.states[state].actions)):
			random_action = random.choice(list(self.states[state].actions.keys()))
			if self.N[state][random_action] < self.learning_iter * self.big_N:
				return random_action
		
		first_action = list(self.states[state].actions.keys())[0]
		q_action = first_action
		highest_Q = self.Q[state][first_action]
		for a in self.states[state].actions:
			if self.Q[state][a] >= highest_Q:
				highest_Q = self.Q[state][a]
				q_action = a
		return q_action
			

	def QLearningAlg(self):
		if self.previous_state == "In": 
			self.previous_state = None
			self.previous_action = None
			self.previous_reward = None
			self.current_action = None
			self.current_state = "Fairway"
			self.current_reward = None
			self.Q["In",None] = 1.0 # reward at "In"

		if self.current_state != "In":
			self.current_reward = 1.0 / (len(list(self.states[self.current_state].actions)) + 1.0)
		else:
			self.current_reward = 1.0

		if self.previous_state is not None:
			# increment n
			self.N[self.previous_state][self.previous_action] += 1
			#get max q in s[a]
			if self.current_state != "In":
				first_action = list(self.states[self.current_state].actions.keys())[0]
				q_action = first_action
				highest_Q = self.Q[self.current_state][first_action]
				for a in self.states[self.current_state].actions:
					if self.Q[self.current_state][a] >= highest_Q:
						highest_Q = self.Q[self.current_state][a]
						q_action = a
			else:
				highest_Q = 1.0
			#self.alpha = (self.N[self.previous_state][self.previous_action] * self.checked) / self.iterations
			self.Q[self.previous_state][self.previous_action] += self.alpha * self.N[self.previous_state][self.previous_action] * \
				(self.previous_reward + self.discount_factor * highest_Q) - self.Q[self.previous_state][self.previous_action]

		#reset
		self.previous_reward = self.current_reward

		if self.current_state != "In":
			self.current_action = self.explore(self.current_state)

		self.previous_state = self.current_state
		if self.current_state != "In":
			self.current_state = self.takeAction(self.current_state,self.current_action)

		self.previous_action = self.current_action

		return self.previous_action	

	# input: action, state
	# output: new state based on the input probabilities
	def takeAction(self,current_state, last_action):
		
		# get a random probability
		probability_list = self.states[current_state].actions[last_action].probabilities
		random_probability = random.randint(1,100)

		# an outcome happens based on the probabilities of action A in state S
		ctr = 0
		traverser = 0
		for i in probability_list:
			traverser += i
			if traverser >= random_probability:
				break
			ctr += 1

		new_state = self.states[current_state].actions[last_action].outcomes[ctr]
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
		diff = abs(q_sum - self.checksum) / self.learning_iter

		if diff < self.epsilon:
			return False
		else:
			self.checksum = q_sum
			return True


	def runQAnalysis(self):
		learning = True
		while learning:
			# every learning_iter iterations:
			# learning = checkSumLearning(self)

			self.QLearningAlg()

			self.iterations += 1
			if self.iterations == self.learning_iter * self.checked:
				learning = self.checkSumLearning()
				self.checked += 1
				print(self.checked)

		return self.getPolicy()