import sys, random
from State import State
from Actions import Action
from QLearningAgent import *
from PolicySearch import *
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

model_free = QLearningAgent(states)

print("MODEL FREE UTILITY FUNCTION:")
print(model_free.runQAnalysis())

print("MODEL FREE Q VALUES: ")
print(model_free.printQ())

#model_based = PolicySearch(states)
print("MODEL FREE TRANSITION VALUES, FOLLOWED BY UTILITY FUNCTION: ")
#print(model_based.runModelBased())



