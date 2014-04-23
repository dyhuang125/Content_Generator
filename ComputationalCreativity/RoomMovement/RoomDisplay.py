from Tkinter import Tk, Canvas, Frame, BOTH

class RoomDisplay(Frame):

	room = [[0.0, 0.0, 0.1, 0.0, 0.0, 0.0, 0.0],
			[0.6, 0.3, 0.0, 0.0, 0.1, 0.0, 0.5]]

	def __init__(self, parent):
		Frame.__init__(self, parent)

		self.parent = parent
		self.initUI()

	def initUI(self):
		self.parent.title("Room")
		self.pack(fill=BOTH, expand=1)

		self.canvas = Canvas(self)
		for level in xrange(0, len(self.room)):
			for grid in xrange(0, len(self.room[level])):
				# Hard coded numbers at the moment
				if self.room[level][grid] == 0.0:
					self.canvas.create_line((grid+1)*50, 50+100*(1+level), (grid+2)*50, 50+100*(1+level), width=2)
				else:
					self.canvas.create_rectangle((grid+1)*50, 50+100*(1+level), (grid+2)*50, 50+100*(1+level-self.room[level][grid]), outline="black", fill="black", width=2)
		self.canvas.pack(fill=BOTH, expand=1)

def main():
	root = Tk()
	ex = RoomDisplay(root)
	root.geometry("450x300+300+300")
	root.mainloop()

if __name__ == '__main__':
	main()
