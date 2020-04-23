import sys, random
from State import State
from Actions import Actions
# import statements

file1 = open("560-project2/assignment2test.txt", "r")
states = {}
# input file: "state/action/possible outcome/probability"

line = file1.readline().strip()
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
		states[split[0]].actions[split[1]] = Actions(split[1])

	# append outcome to state.action.outcome
	states[split[0]].actions[split[1]].outcomes.append(split[2])

	# append probability to state.action.probability
	states[split[0]].actions[split[1]].probabilities.append(int(float(split[3])*100))

	line = file1.readline().strip()

# first TO DO: get the program to where it can reliably play golf before introducing anything interesting. 
def playGolf():

	score = 0
	ball = start
	while ball != "In":
		# random action to be substituted with some sort of machine learning thing - maybe? could keep it at the start at least
		x = len(states[ball].actions)
		random_action = random.randint(0,x-1)
		act_keys = list(states[ball].actions.keys())
		action_taken = act_keys[random_action]

		probability_list = states[ball].actions[action_taken].probabilities
		ctr = 0
		traverser = 0
		random_probability = random.randint(1,100)

		# choose an outcome based on the probably outcomes of the action
		for i in probability_list:
			traverser += i
			round(traverser, 3)
			if traverser >= random_probability:
				break
			ctr += 1

		ball = states[ball].actions[action_taken].outcomes[ctr]
		score += 1
		# use random outcome (and action for now) to determine what happens		

	# keep a log of the shots and then go back and add the scores.
	return score

averagescore = 0
tests = 100000
for x in range(0,tests):
	averagescore += playGolf()
averagescore = averagescore / tests
print(averagescore)