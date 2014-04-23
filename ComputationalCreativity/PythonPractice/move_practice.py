from Tkinter import Tk, Canvas, Frame, BOTH

class Move(Frame):

	def __init__(self, parent):
		Frame.__init__(self, parent)

		self.parent = parent
		self.initUI()
		self.animate()

	def initUI(self):
		self.parent.title("Move")
		self.pack(fill=BOTH, expand=1)

		self.canvas = Canvas(self)
		self.oval = self.canvas.create_oval(40, 10, 110, 80, outline="black", width=2)
		self.canvas.pack(fill=BOTH, expand=1)

	def animate(self):
		location = self.canvas.coords(self.oval)
		self.canvas.coords(self.oval, location[0]+2.5, location[1],
								location[2]+2.5, location[3])
		self.after(1000, self.animate)

def main():
	root = Tk()
	ex = Move(root)
	root.geometry("1000x250+300+300")
	root.mainloop()

if __name__ == '__main__':
	main()