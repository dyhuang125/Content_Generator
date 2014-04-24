import random as random

class StateMachine():

	def __init__(self, StateSpace, StartState):
		self.stateSpace = StateSpace
		self.currentState = StartState

	def next(self):
		# Compute transition probabilities
		probabilities = []

		# Probability of not moving
		probabilities.append((self.currentState, 1.0))

		# Probability of moving left
		current_x = self.currentState[0]-1
		probability = 1.0/3.0
		while True:
			if current_x < 0:
				break
			else:
				probabilities.append(((current_x, self.currentState[1]), probability))
				current_x = current_x - 1
				probability = probability/3.0

		# Probability of moving right
		current_x = self.currentState[0]+1
		probability = 1.0/3.0
		while True:
			if current_x >= len(self.stateSpace[self.currentState[1]]):
				break
			else:
				probabilities.append(((current_x, self.currentState[1]), probability))
				current_x = current_x + 1
				probability = probability/3.0

		# Probability of moving up
		if self.currentState[1] < len(self.stateSpace)-1 and \
		  (self.currentState[0] == 0 or \
		  self.currentState[0] == len(self.stateSpace[self.currentState[1]])-1):
			probabilities.append(((self.currentState[0], self.currentState[1]+1), 1.0/3.0))

		# Probability of falling down
		if self.currentState[1] > 0:
			probabilities.append(((self.currentState[0], self.currentState[1]-1), 1.0/18.0))
			if self.currentState[0] - 1 >= 0:
				probabilities.append(((self.currentState[0]-1, self.currentState[1]-1), 1.0/18.0))
			if self.currentState[0] + 1 < len(self.stateSpace[self.currentState[1]]):
				probabilities.append(((self.currentState[0]+1, self.currentState[1]-1), 1.0/18.0))
			if self.currentState[0] - 2 >= 0:	
				probabilities.append(((self.currentState[0]-2, self.currentState[1]-1), 1.0/18.0))
			if self.currentState[0] + 2 < len(self.stateSpace[self.currentState[1]]):
				probabilities.append(((self.currentState[0]+2, self.currentState[1]-1), 1.0/18.0))

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

				distance = calculate_distance()
				left = math.floor(distance/2.0)
				right = math.ceil(distance/2.0)

				# If top-down transition
				if newState[1] < self.currentState[1]:
					if random.random() > 0.5:
						# One character high, one character low
						if random.random() > 0.5:
							# Left high, right low
							character_one = (max(0, newState[0]-left), self.currentState[1])
							character_two = (min(len(self.stateSpace[newState[1]]), newState[0]+right), newState[1])
						else:
							# Left low, right high
							character_one = (max(0, newState[0]-left), self.currentState[1])
							character_two = (min(len(self.stateSpace[newState[1]]), newState[0]+right), newState[1])
						self.currentState = newState
						if random.random() > 0.5:
							return (character_one, character_two)
						else:
							return (character_two, character_one)

				# Normal
				if self.currentState[1] >= len(self.stateSpace):
					# If top floor
					character_one = (max(0, newState[0]-left), self.currentState[1])
					character_two = (min(len(self.stateSpace[newState[1]]), newState[0]+right), newState[1])
				else:
					if left > newState[0]:
						character_one = ()

				self.currentState = newState
				return (character_one, character_two)

	# Calculate weighted distance between 0 and 8
	def calculate_distance(self):
		probabilities = []
		probability = 1.0
		for i in xrange(0, 9):
			probabilities.append(i, probability)
			probability = probability/3.0

		sum_of_prob = 0.0
		for p in xrange(0, 9):
			sum_of_prob = sum_of_prob + probabilities[p][1]
		index = random.uniform(0.0, sum_of_prob)
		for p in xrange(0, 9):
			index = index - probabilities[p][1]
			if index <= 0.0:
				return p

def main():
	room = [[0.0, 0.0, 0.1, 0.0, 0.0, 0.0, 0.0],
			[0.6, 0.3, 0.0, 0.0, 0.1, 0.0, 0.5]]
	start = (3, 0)
	sm = StateMachine(room, start)

	while True:
		read_input = raw_input("Press for Next State")
		sm.next()
		print sm.currentState

if __name__ == '__main__':
	main()
