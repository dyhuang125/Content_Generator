from Tkinter import Tk, Canvas, Frame, BOTH

class Example(Frame):

	def __init__(self, parent):
		Frame.__init__(self, parent)

		self.parent = parent
		self.initUI()

	def initUI(self):
		self.parent.title("Shapes")
		self.pack(fill=BOTH, expand=1)
		
		canvas = Canvas(self)
		canvas.create_oval(40, 10, 110, 80, outline="black", width=2)
		canvas.create_line(75, 80, 75, 180, width=2)		

		canvas.pack(fill=BOTH, expand=1)

def main():
	root = Tk()
	ex = Example(root)
	root.geometry("200x250+300+300")
	root.mainloop()

if __name__ == '__main__':
	main()