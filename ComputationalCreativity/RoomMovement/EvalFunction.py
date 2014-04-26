import StateMachine as StateMachine

# Static variables
LEFT = 0
RIGHT = 1

class EvalFunction():

	def __init__(self, room, ActionList):
		self.room = room
		self.actionList = ActionList
		self.evaluate()

	def evaluate(self):
		self.score = 0.0
		self.score = self.score + 3*self.character_one_constant_movement()
		self.score = self.score + 3*self.character_two_constant_movement()
		self.score = self.score + 5*self.no_standing_still()
		self.score = self.score + 3*self.character_one_directional_movement()
		self.score = self.score + 3*self.character_two_directional_movement()
		self.score = self.score + self.overall_constant_movement()
		self.score = self.score + 3*self.different_floors()
		self.score = self.score + self.constant_action()
		self.score = self.score + self.enough_separation()

	def character_one_constant_movement(self):
		score = 0

		for i in xrange(1, len(self.actionList)):
			if self.actionList[i][0] == self.actionList[i-1][0] and \
			  (self.actionList[i][3] != 0 or \
			  self.actionList[i-1][3] != 0):
				score = score-1

		return score

	def character_two_constant_movement(self):
		score = 0

		for i in xrange(1, len(self.actionList)):
			if self.actionList[i][1] == self.actionList[i-1][1] and \
			  (self.actionList[i][3] != 0 or \
			  self.actionList[i-1][3] != 0):
				score = score-1

		return score

	def no_standing_still(self):
		score = 0

		for i in xrange(1, len(self.actionList)):
			if self.actionList[i] == self.actionList[i-1]:
				score = score-1

		return score

	def character_one_directional_movement(self):
		score = 0

		streak = 0
		direction = -1
		for i in xrange(1, len(self.actionList)):
			if self.actionList[i][0][0] < self.actionList[i-1][0][0]:
				if direction == LEFT:
					streak = streak+1
					if streak > 2:
						score = score+1
				else:
					direction = LEFT
					streak = 0
			elif self.actionList[i][0][0] > self.actionList[i-1][0][0]:
				if direction == RIGHT:
					streak = streak+1
					if streak > 2:
						score = score+1
				else:
					direction = LEFT
					streak = 0

		return score

	def character_two_directional_movement(self):
		score = 0

		streak = 0
		direction = -1
		for i in xrange(1, len(self.actionList)):
			if self.actionList[i][1][0] < self.actionList[i-1][1][0]:
				if direction == LEFT:
					streak = streak+1
					if streak > 2:
						score = score+1
				else:
					direction = LEFT
					streak = 0
			elif self.actionList[i][1][0] > self.actionList[i-1][1][0]:
				if direction == RIGHT:
					streak = streak+1
					if streak > 2:
						score = score+1
				else:
					direction = LEFT
					streak = 0

		return score

	def overall_constant_movement(self):
		score = 0

		states = []
		for y in xrange(0, len(self.room)):
			states.append([0]*len(self.room[0]))

		for i in xrange(0, len(self.actionList)):
			x_coord = self.actionList[i][2][0]
			y_coord = self.actionList[i][2][1]
			states[y_coord][x_coord] = states[y_coord][x_coord]+1

		for y in xrange(0, len(states)):
			for x in xrange(0, len(states[0])):
				if states[y][x] >= 3:
					score = score-1
				if states[y][x] >= 5:
					score = score-(states[y][x]-4)

		return score

	def different_floors(self):
		score = 0

		floors = [0]*len(self.room)
		for i in xrange(0, len(self.actionList)):
			floors[self.actionList[i][2][1]] = floors[self.actionList[i][2][1]]+1

		for f in xrange(0, len(floors)):
			if floors[f] > 0:
				score = score+1
			if floors[f] > 3:
				score = score+1
			if floors[f] > 6:
				score = score+1

		return score

	def constant_action(self):
		score = 0

		streak = 0
		for i in xrange(0, len(self.actionList)):
			if self.actionList[i][3] > 0:
				streak = streak+1
			else:
				streak = 0

			if streak > 1:
				score = score - (streak-1)

		return score

	def enough_separation(self):
		score = 0

		streak = 0
		for i in xrange(0, len(self.actionList)):
			if self.actionList[i][3] == 0:
				streak = streak+1
			else:
				streak = 0

			if streak > 3:
				score = score - (streak-3)

		return score

def main():
	room = [[0.6, 0.3, 0.0, 0.0, 0.1, 0.0, 0.5],
			[0.3, 0.0, 0.1, 0.0, 0.0, 0.0, 0.3],
			[0.0, 0.1, 0.0, 0.0, 0.0, 0.1, 0.0]]

	sm = StateMachine.StateMachine(room)
	actionList = []
	for i in xrange(0, 30):
		actionList.append(sm.next())

	ef = EvalFunction(room, actionList)

if __name__ == '__main__':
	main()