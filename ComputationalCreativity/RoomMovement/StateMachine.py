import math as math
import random as random

EXPONENT = 2.5

class StateMachine():

	def __init__(self, StateSpace):
		self.stateSpace = StateSpace
		start_x = random.randint(0, len(StateSpace[0])-1)
		start_y = random.randint(0, len(StateSpace)-1)
		self.currentState = (start_x, start_y)

	def next(self):
		# Compute transition probabilities
		probabilities = []

		# Probability of not moving
		probabilities.append((self.currentState, 1.0))

		# Probability of moving left
		current_x = self.currentState[0]-1
		probability = 1.0/EXPONENT
		while True:
			if current_x < 0:
				break
			else:
				probabilities.append(((current_x, self.currentState[1]), probability))
				current_x = current_x - 1
				probability = probability/EXPONENT

		# Probability of moving right
		current_x = self.currentState[0]+1
		probability = 1.0/EXPONENT
		while True:
			if current_x >= len(self.stateSpace[self.currentState[1]]):
				break
			else:
				probabilities.append(((current_x, self.currentState[1]), probability))
				current_x = current_x + 1
				probability = probability/EXPONENT

		# Probability of moving up
		if self.currentState[1] < len(self.stateSpace)-1 and \
		  (self.currentState[0] == 0 or \
		  self.currentState[0] == len(self.stateSpace[self.currentState[1]])-1):
			probabilities.append(((self.currentState[0], self.currentState[1]+1), 1.0/EXPONENT))

		# Probability of falling down
		if self.currentState[1] > 0:
			probabilities.append(((self.currentState[0], self.currentState[1]-1), 1.0/(2*EXPONENT**2)))
			if self.currentState[0] - 1 >= 0:
				probabilities.append(((self.currentState[0]-1, self.currentState[1]-1), 1.0/(2*EXPONENT**2)))
			if self.currentState[0] + 1 < len(self.stateSpace[self.currentState[1]]):
				probabilities.append(((self.currentState[0]+1, self.currentState[1]-1), 1.0/(2*EXPONENT**2)))
			if self.currentState[0] - 2 >= 0:	
				probabilities.append(((self.currentState[0]-2, self.currentState[1]-1), 1.0/(2*EXPONENT**2)))
			if self.currentState[0] + 2 < len(self.stateSpace[self.currentState[1]]):
				probabilities.append(((self.currentState[0]+2, self.currentState[1]-1), 1.0/(2*EXPONENT**2)))

		# Transition
		sum_of_prob = 0.0
		for p in xrange(0, len(probabilities)):
			sum_of_prob = sum_of_prob + probabilities[p][1]
		index = random.uniform(0.0, sum_of_prob)
		for p in xrange(0, len(probabilities)):
			index = index - probabilities[p][1]
			if index <= 0.0:
				# Calculate character specific states
				newState = probabilities[p][0]

				distance = self.calculate_distance()
				left = int(math.floor(distance/2.0))
				right = int(math.ceil(distance/2.0))

				# If top-down transition
				if newState[1] < self.currentState[1]:
					if random.random() > 0.5:
						# One character high, one character low
						if random.random() > 0.5:
							# Left high, right low
							character_one = (max(0, newState[0]-left), self.currentState[1])
							character_two = (min(len(self.stateSpace[newState[1]])-1, newState[0]+right), newState[1])
						else:
							# Left low, right high
							character_one = (max(0, newState[0]-left), self.currentState[1])
							character_two = (min(len(self.stateSpace[newState[1]])-1, newState[0]+right), newState[1])
						self.currentState = newState
						if random.random() > 0.5:
							return (character_one, character_two, newState, distance, False)
						else:
							return (character_two, character_one, newState, distance, False)

				# Normal
				wallhop = False
				if newState[1] >= len(self.stateSpace)-1:
					# If top floor
					character_one = (max(0, newState[0]-left), self.currentState[1])
					character_two = (min(len(self.stateSpace[newState[1]])-1, newState[0]+right), newState[1])
				else:
					if left > newState[0]:
						character_one = (left-newState[0], newState[1]+1)
						wallhop = True
					else:
						character_one = (newState[0]-left, newState[1])
					if right+newState[0] >= len(self.stateSpace[self.currentState[1]]):
						newRight = right+newState[0]-len(self.stateSpace[self.currentState[1]])
						character_two = (newRight, newState[1]+1)
						wallhop = True
					else:
						character_two = (newState[0]+right, newState[1])

				self.currentState = newState
				if random.random() > 0.5:
					return (character_one, character_two, newState, distance, wallhop)
				else:
					return (character_two, character_one, newState, distance, wallhop)

	# Calculate weighted distance between 0 and 4
	def calculate_distance(self):
		probabilities = []
		probability = 1.0
		for i in xrange(0, 5):
			probabilities.append((i, probability))
			probability = probability/3.0

		sum_of_prob = 0.0
		for p in xrange(0, 5):
			sum_of_prob = sum_of_prob + probabilities[p][1]
		index = random.uniform(0.0, sum_of_prob)
		for p in xrange(0, 5):
			index = index - probabilities[p][1]
			if index <= 0.0:
				return p

def main():
	room = [[0.0, 0.0, 0.1, 0.0, 0.0, 0.0, 0.0],
			[0.6, 0.3, 0.0, 0.0, 0.1, 0.0, 0.5]]
	sm = StateMachine(room)

	while True:
		read_input = raw_input("Press for Next State")
		print sm.next()

if __name__ == '__main__':
	main()
