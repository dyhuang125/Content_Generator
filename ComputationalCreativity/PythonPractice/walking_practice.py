from Tkinter import Tk, Canvas, Frame, BOTH
import math as math
PI = 3.1415926

def distance(x1,y1,x2,y2):
	return math.sqrt((x1-x2)**2+(y1-y2)**2)

class Walking(Frame):
	def __init__(self, parent):
		Frame.__init__(self, parent)

		self.parent = parent
		self.init()
		self.animate()

	def init(self):
		self.parent.title("Walking")
		self.pack(fill=BOTH, expand=1)

		self.canvas = Canvas(self)

		self.current_iteration = 0
		self.num_iterations = 100

		self.segment_length = 50.0

		# Start Coordinates
		self.start_hip = [50.0,120.0]
		self.start_left_foot = [80.0,200.0]
		self.start_right_foot = [20.0,200.0]

		# End Coordinates
		self.end_hip = [80.0,105.0]
		self.end_left_foot = [80.0,200.0]
		self.end_right_foot = [80.0,180.0]

		# Calculate starting left leg
		leg_angle = math.atan2(self.start_left_foot[1]-self.start_hip[1],
							   self.start_left_foot[0]-self.start_hip[0])
		leg_length = distance(self.start_hip[0], self.start_hip[1],
							  self.start_left_foot[0], self.start_left_foot[1])
		segment_angle = math.acos((leg_length/2)/self.segment_length)
		self.current_left_ankle = leg_angle + segment_angle
		self.current_left_knee = 2*(PI/2 - segment_angle)
		self.current_left_hip = (PI/2 - leg_angle) + segment_angle

		# Calculate starting right leg
		leg_angle = math.atan2(self.start_right_foot[1]-self.start_hip[1],
							   self.start_right_foot[0]-self.start_hip[0])
		leg_length = distance(self.start_hip[0], self.start_hip[1],
							  self.start_right_foot[0], self.start_right_foot[1])
		segment_angle = math.acos((leg_length/2)/self.segment_length)
		self.current_right_ankle = leg_angle + segment_angle
		self.current_right_knee = 2*(PI/2 - segment_angle)
		self.current_right_hip = (PI/2 - leg_angle) + segment_angle

		# Calculate ending left leg
		leg_length = distance(self.end_hip[0], self.end_hip[1],
							  self.end_left_foot[0], self.end_left_foot[1])
		segment_angle = math.acos((leg_length/2)/self.segment_length)
		self.end_left_ankle = PI/2 + segment_angle
		self.end_left_knee = 2*(PI/2 - segment_angle)
		self.end_left_hip = segment_angle

		# Calculate ending right leg
		leg_length = distance(self.end_hip[0], self.end_hip[1],
							  self.end_right_foot[0], self.end_right_foot[1])
		segment_angle = math.acos((leg_length/2)/self.segment_length)
		self.end_right_ankle = PI/2 + segment_angle
		self.end_right_knee = 2*(PI/2 - segment_angle)
		self.end_right_hip = segment_angle

		self.dif_left_ankle = (self.end_left_ankle - self.current_left_ankle)/self.num_iterations
		self.dif_left_knee = (self.end_left_knee - self.current_left_knee)/self.num_iterations
		self.dif_left_hip = (self.end_left_hip - self.current_left_hip)/self.num_iterations

		self.dif_right_ankle = (self.end_right_ankle - self.current_right_ankle)/self.num_iterations
		self.dif_right_knee =(self.end_right_knee - self.current_right_knee)/self.num_iterations
		self.dif_right_hip = (self.end_right_hip - self.current_right_hip)/self.num_iterations

		# Calculate starting position
		knee_y_dif = self.segment_length*math.sin(self.current_left_ankle)
		knee_x_dif = self.segment_length*math.cos(self.current_left_ankle)
		knee_x = self.start_left_foot[0]-knee_x_dif
		knee_y = self.start_left_foot[1]-knee_y_dif
		self.left_lower_leg = self.canvas.create_line(self.start_left_foot[0],
													  self.start_left_foot[1],
													  knee_x,
													  knee_y,
													  width=2)
		self.left_upper_leg = self.canvas.create_line(knee_x,
													  knee_y,
													  self.start_hip[0],
													  self.start_hip[1],
													  width=2)
		knee_y_dif = self.segment_length*math.sin(self.current_right_ankle)
		knee_x_dif = self.segment_length*math.cos(self.current_right_ankle)
		knee_x = self.start_right_foot[0]-knee_x_dif
		knee_y = self.start_right_foot[1]-knee_y_dif
		self.right_lower_leg = self.canvas.create_line(self.start_right_foot[0],
													   self.start_right_foot[1],
													   knee_x,
													   knee_y,
													   width=2)
		self.right_upper_leg = self.canvas.create_line(knee_x,
													   knee_y,
													   self.start_hip[0],
													   self.start_hip[1],
													   width=2)
		self.torso = self.canvas.create_line(self.start_hip[0],
											 self.start_hip[1],
											 self.start_hip[0],
											 self.start_hip[1]-80.0,
											 width=2)


		self.canvas.pack(fill=BOTH, expand=1)

	def animate(self):
		# Left lower leg
		self.current_left_ankle = self.current_left_ankle + self.dif_left_ankle
		knee_y_dif = self.segment_length*math.sin(self.current_left_ankle)
		knee_x_dif = self.segment_length*math.cos(self.current_left_ankle)
		knee_x = self.start_left_foot[0]-knee_x_dif
		knee_y = self.start_left_foot[1]-knee_y_dif
		self.canvas.coords(self.left_lower_leg, self.start_left_foot[0],
												self.start_left_foot[1],
												knee_x,
												knee_y)

		# Left upper leg
		self.current_left_knee = self.current_left_knee + self.dif_left_knee
		aligned_angle = self.current_left_knee - (PI - self.current_left_ankle)
		hip_y_dif = self.segment_length*math.sin(aligned_angle)
		hip_x_dif = self.segment_length*math.cos(aligned_angle)
		hip_x = knee_x - hip_x_dif
		hip_y = knee_y - hip_y_dif
		self.canvas.coords(self.left_upper_leg, knee_x,
												knee_y,
												hip_x,
												hip_y)

		# Right upper leg
		self.current_right_hip = self.current_right_hip + self.dif_right_hip
		aligned_angle = PI/2 - self.current_right_hip
		hip_y_dif = self.segment_length*math.sin(aligned_angle)
		hip_x_dif = self.segment_length*math.cos(aligned_angle)
		knee_x = hip_x + hip_x_dif
		knee_y = hip_y + hip_y_dif
		self.canvas.coords(self.right_upper_leg, knee_x,
												 knee_y,
												 hip_x,
												 hip_y)

		# Right lower leg
		self.current_right_knee = self.current_right_knee + self.dif_right_knee
		aligned_angle = self.current_right_knee - (PI/2 - self.current_right_hip)
		knee_y_dif = self.segment_length*math.sin(aligned_angle)
		knee_x_dif = self.segment_length*math.cos(aligned_angle)
		foot_x = knee_x - knee_x_dif
		foot_y = knee_y + knee_y_dif
		self.canvas.coords(self.right_lower_leg, foot_x,
												 foot_y,
												 knee_x,
												 knee_y)

		# Torso
		self.canvas.coords(self.torso, hip_x,
									   hip_y,
									   hip_x,
									   hip_y-80.0)

		self.current_iteration = self.current_iteration + 1
		if self.current_iteration < self.num_iterations:
			self.after(10, self.animate)

def main():
	root = Tk()
	ex = Walking(root)
	root.geometry("200x250+300+300")
	root.mainloop()

if __name__ == '__main__':
	main()