import random
from State import State
from Actions import Action
class PolicySearch():
	def __init__(self, states):
		self.original = states
		self.model = {}
		# copy states and actions to model. Don't copy outcomes or probabilities
		for s in states:
			self.model[s] = State(s)
			for a in states[s].actions:
				self.model[s].actions[a] = Action(a)
		self.num_iterations = 10000


	# input: real state model,transitionless model
	# output: None, but transition values will now be found in 
	def getTransitionValues(self):
		for state in self.model:
			for action in self.model[state].actions:
				for i in range(0,self.num_iterations):
					result = self.simulateAction(state, action)
					if result not in self.model[state].actions[action].num_outcomes:
						self.model[state].actions[action].num_outcomes[result] = 0
					self.model[state].actions[action].num_outcomes[result] += 1

		for state in self.model:
			for action in self.model[state].actions:
				for outcome_num in self.model[state].actions[action].num_outcomes:
					if outcome_num not in self.model[state].actions[action].new_prob:
						self.model[state].actions[action].new_prob[outcome_num] = self.model[state].actions[action].num_outcomes[outcome_num] / \
							self.num_iterations
						self.model[state].actions[action].probabilities.append(int(float(self.model[state].actions[action].num_outcomes[outcome_num] / \
							self.num_iterations)*100))
						self.model[state].actions[action].outcomes.append(outcome_num)

		return None

	# prints transition values
	def printTransitionValues(self):
		for state in self.model:
			for act in self.model[state].actions:
				for outcome_num in self.model[state].actions[act].num_outcomes:
					print(state+"/"+act+"/"+outcome_num+"/"+str(self.model[state].actions[act].new_prob[outcome_num]))
		return None

	# input: state, action
	# output: resulting state based on the official input
	def simulateAction(self, state, action):
		# get a random probability
		probability_list = self.original[state].actions[action].probabilities
		random_probability = random.randint(1,100)
		# an outcome happens based on the probabilities of action A in state S
		ctr = 0
		traverser = 0
		for i in probability_list:
			traverser += i
			if traverser >= random_probability:
				break
			ctr += 1

		resulting_state = self.original[state].actions[action].outcomes[ctr]
		return resulting_state

	# input: state, action
	# output: resulting state based on the model
	def simulateActionInModel(self, state, action):
		probability_list = self.model[state].actions[action].probabilities
		random_probability = random.randint(1,100)
		# an outcome happens based on the probabilities of action A in state S
		ctr = 0
		traverser = 0
		for i in probability_list:
			traverser += i
			if traverser >= random_probability:
				break
			ctr += 1
		if ctr == len(self.model[state].actions[action].probabilities):
			ctr -= 1
		resulting_state = self.model[state].actions[action].outcomes[ctr]
		return resulting_state


	# plays golf (taking random actions) from the start-action point in the model. records remaining hits in action
	# recursively implemented! 
	def remainingHits(self, state, action):
		if state == "In":
			return 0
		# outcome based on calcalculated_probabilities
		new_state = self.simulateActionInModel(state, action)

		if new_state == "In":
			return 1
		new_action = self.chooseActionRandomly(new_state)
		return 1 + self.remainingHits(new_state, new_action)

	# choose action randomly
	def chooseActionRandomly(self, state):
		if len(self.model[state].actions) is 1:
			return list(self.model[state].actions.keys())[0]

		random_action = random.choice(list(self.model[state].actions.keys()))
		return random_action

	# calculates average remaining hits that it takes to get a ball in the hole after an action is taken
	# in practice - this is calculating the REWARD function. 
	def calcAverageRemainingHits(self):
		for state in self.model:
			for action in self.model[state].actions:
				for i in range(0,self.num_iterations):
					self.model[state].actions[action].swings += 1
					self.model[state].actions[action].shots_to_in += self.remainingHits(state, action)
				# update reward function
				self.model[state].actions[action].reward = 1.0 / (self.model[state].actions[action].shots_to_in / self.model[state].actions[action].swings)
		return None

	# maximize reward values ('shots to in')
	def calcUtilityFunction(self):
		utility_function = {}
		for s in self.model:
			reward = 0
			to_take = None
			for a in self.model[s].actions:
				if self.model[s].actions[a].reward > reward:
					reward = self.model[s].actions[a].reward
					to_take = a
			utility_function[s] = to_take
		return utility_function

	# runs program
	def runModelBased(self):
		self.getTransitionValues()
		self.calcAverageRemainingHits()
		self.printTransitionValues()
		return self.calcUtilityFunction()

