from Tkinter import Tk, Canvas, Frame, BOTH
import StateMachine as StateMachine
import EvalFunction as EvalFunction

# Static variables
LEFT = 0
RIGHT = 1

NUM_ITERATIONS = 50
SMALL_VALUE = -200

def switchSides(side):
	if side == LEFT:
		return RIGHT
	else:
		return LEFT

class RoomDisplay(Frame):

	def __init__(self, parent, actionList, room):
		Frame.__init__(self, parent)

		self.actionList = actionList
		self.room = room

		self.parent = parent
		self.initUI()
		self.displayMotion()

	def initUI(self):
		self.parent.title("Room")
		self.pack(fill=BOTH, expand=1)

		self.canvas = Canvas(self)
		for level in xrange(0, len(self.room)):
			for grid in xrange(0, len(self.room[level])):
				if self.room[level][grid] == 0.0:
					self.canvas.create_line((grid+1)*50, 50+100*(len(self.room)-level), (grid+2)*50, 50+100*(len(self.room)-level), width=2)
				else:
					self.canvas.create_rectangle((grid+1)*50, 50+100*(len(self.room)-level), (grid+2)*50, 50+100*(len(self.room)-level-self.room[level][grid]), outline="black", fill="black", width=2)

		self.canvas.create_line(50, 50, 50, 50+100*len(self.room), width=2)
		self.canvas.create_line(400, 50, 400, 50+100*len(self.room), width=2)

		character_one = self.characterXYCoordinates(self.actionList[0][0], LEFT)
		character_two = self.characterXYCoordinates(self.actionList[0][1], RIGHT)
		self.character_one_side = LEFT
		self.character_two_side = RIGHT
		self.character_one = self.canvas.create_oval(character_one[0], character_one[1], character_one[2], character_one[3], outline="red", fill="red", width=2)
		self.character_two = self.canvas.create_oval(character_two[0], character_two[1], character_two[2], character_two[3], outline="blue", fill="blue", width=2)
		self.currentAction = 0

		self.canvas.pack(fill=BOTH, expand=1)

	def characterXYCoordinates(self, state, side):
		left_boundary = 52.5 + 50*state[0]
		if side == LEFT:
			left_boundary = left_boundary + 25

		bottom_boundary = 50 + 100*(len(self.room)-state[1]-self.room[state[1]][state[0]]) - 20
		
		return (left_boundary, bottom_boundary, left_boundary+20, bottom_boundary-20)

	def displayMotion(self):
		if self.currentAction < len(self.actionList)-1:
			print self.actionList[self.currentAction+1]

			if self.actionList[self.currentAction][2] == self.actionList[self.currentAction+1][2] and \
			  self.actionList[self.currentAction][3] == 0 and \
			  self.actionList[self.currentAction+1][3] == 0:
				# Switch sides
				old_character_one = self.characterXYCoordinates(self.actionList[self.currentAction][0], self.character_one_side)
				old_character_two = self.characterXYCoordinates(self.actionList[self.currentAction][1], self.character_two_side)

				self.character_one_side = switchSides(self.character_one_side)
				self.character_two_side = switchSides(self.character_two_side)

				new_character_one = self.characterXYCoordinates(self.actionList[self.currentAction+1][0], self.character_one_side)
				new_character_two = self.characterXYCoordinates(self.actionList[self.currentAction+1][1], self.character_two_side)
			else:
				old_character_one = self.characterXYCoordinates(self.actionList[self.currentAction][0], self.character_one_side)
				old_character_two = self.characterXYCoordinates(self.actionList[self.currentAction][1], self.character_two_side)
				new_character_one = self.characterXYCoordinates(self.actionList[self.currentAction+1][0], self.character_one_side)
				new_character_two = self.characterXYCoordinates(self.actionList[self.currentAction+1][1], self.character_two_side)

			self.animate(self.character_one, old_character_one, new_character_one, 0, 0)
			self.animate(self.character_two, old_character_two, new_character_two, 0, 1)
			self.currentAction = self.currentAction+1

	def animate(self, character, start, end, iteration, thread_index):
		interpolate0 = start[0] + (end[0]-start[0])*iteration/NUM_ITERATIONS
		interpolate1 = start[1] + (end[1]-start[1])*iteration/NUM_ITERATIONS
		interpolate2 = start[2] + (end[2]-start[2])*iteration/NUM_ITERATIONS
		interpolate3 = start[3] + (end[3]-start[3])*iteration/NUM_ITERATIONS

		self.canvas.coords(character, interpolate0, interpolate1, interpolate2, interpolate3)

		if iteration < NUM_ITERATIONS:
			self.after(10, self.animate, character, start, end, iteration+1, thread_index)
		elif thread_index == 0:
			self.after(10, self.displayMotion)

def main():
	room = [[0.6, 0.3, 0.0, 0.0, 0.1, 0.0, 0.5],
			[0.3, 0.0, 0.1, 0.0, 0.0, 0.0, 0.3],
			[0.0, 0.1, 0.0, 0.0, 0.0, 0.1, 0.0]]

	# actionList = [((3,0),(3,0),(3,0),0),
	# 			  ((5,0),(4,0),(4,0),1),
	# 			  ((6,0),(6,0),(6,0),0),
	# 			  ((6,0),(6,0),(6,0),0)]

	top_score = SMALL_VALUE
	for iteration in xrange(0, 50):
		sm = StateMachine.StateMachine(room)
		actionList = []
		for i in xrange(0, 30):
			actionList.append(sm.next())

		ef = EvalFunction.EvalFunction(room, actionList)
		if ef.score > top_score:
			top_score = ef.score
			top_actionList = actionList

	root = Tk()
	ex = RoomDisplay(root, top_actionList, room)
	root.geometry("450x400+300+300")
	root.mainloop()

if __name__ == '__main__':
	main()
