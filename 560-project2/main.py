import sys, random
from State import State
from Actions import Action
from QLearningAgent import *
# import statements - I added one line to the test file to account for the lack of "In" state. 

file1 = open("560-project2/assignment2test.txt", "r")
states = {}
# input file: "state/action/possible outcome/probability"

line = file1.readline().strip()
# golf ball will start at the first state listed. 
start = "hi"
while (1):
	if (not line):
		break
	split = line.split("/")
	if start == "hi":
		start = split[0]
	if split[0] not in states:
		states[split[0]] = State(split[0])
	if split[1] not in states[split[0]].actions:
		states[split[0]].actions[split[1]] = Action(split[1])

	# append outcome to state.action.outcome
	states[split[0]].actions[split[1]].outcomes.append(split[2])

	# append probability to state.action.probability
	states[split[0]].actions[split[1]].probabilities.append(int(float(split[3])*100))

	line = file1.readline().strip()
# input file doesn't have "In" state. - might not do this.
# In/Begin/Fairway/1.00

# first TO DO: get the program to where it can reliably play golf before introducing anything interesting. 
def playGolf():

	score = 0
	ball = start
	while ball != "In":

		# Select random action. 
		x = len(states[ball].actions)
		random_action = random.randint(0,x-1)
		act_keys = list(states[ball].actions.keys())
		action_taken = act_keys[random_action]

		# get a random probability
		probability_list = states[ball].actions[action_taken].probabilities
		random_probability = random.randint(1,100)

		# choose an outcome based on the probabilities of the action
		ctr = 0
		traverser = 0
		for i in probability_list:
			traverser += i
			if traverser >= random_probability:
				break
			ctr += 1

		ball = states[ball].actions[action_taken].outcomes[ctr]
		score += 1
		
		# use random outcome (and action for now) to determine what happens

	# keep a log of the shots and then go back and add the scores.
	return score

x = QLearningAgent(states)
print(x.runQAnalysis())



