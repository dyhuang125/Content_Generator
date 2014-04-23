from Tkinter import Tk, Canvas, Frame, BOTH
import math as math
PI = 3.1415926

def distance(x1,y1,x2,y2):
	return math.sqrt((x1-x2)**2+(y1-y2)**2)

class ConstraintSolver(Frame):
	def __init__(self, parent):
		Frame.__init__(self, parent)

		self.parent = parent
		self.init()
		self.animate()

	def init(self):
		self.parent.title("ConstraintSolver")
		self.pack(fill=BOTH, expand=1)

		self.canvas = Canvas(self)

		self.current_iteration = 0
		self.num_iterations = 100

		# Start Coordinates
		self.start_hip = [50.0, 120.0]
		self.start_left_foot = [80.0, 200.0]
		self.start_right_foot = [20.0, 200.0]

		# End Coordinates
		self.end_hip = [80.0, 105.0]
		self.end_left_foot = [80.0, 200.0]
		self.end_right_foot = [80.0, 185.0]

		self.segment_length = 50.0

		# Variables
		self.left_leg_length = distance(self.start_hip[0], self.start_hip[1],
										self.start_left_foot[0], self.start_left_foot[1])
		self.left_leg_angle = math.atan2(self.start_left_foot[1]-self.start_hip[1],
										 self.start_left_foot[0]-self.start_hip[0])
		self.right_leg_length = distance(self.start_hip[0], self.start_hip[1],
							 			 self.start_right_foot[0], self.start_right_foot[1])
		self.right_leg_angle = math.atan2(self.start_right_foot[1]-self.start_hip[1],
										 self.start_right_foot[0]-self.start_hip[0])

		# Calculate Starting Positions
		left_segment_angle = math.acos((self.left_leg_length/2)/self.segment_length)
		left_knee_x_dif = self.segment_length*math.cos(self.left_leg_angle+left_segment_angle)
		left_knee_y_dif = self.segment_length*math.sin(self.left_leg_angle+left_segment_angle)
		left_knee_x = self.start_left_foot[0]-left_knee_x_dif
		left_knee_y = self.start_left_foot[1]-left_knee_y_dif

		right_segment_angle = math.acos((self.right_leg_length/2)/self.segment_length)
		right_knee_x_dif = self.segment_length*math.cos(self.right_leg_angle+right_segment_angle)
		right_knee_y_dif = self.segment_length*math.sin(self.right_leg_angle+right_segment_angle)
		right_knee_x = self.start_right_foot[0]-right_knee_x_dif
		right_knee_y = self.start_right_foot[1]-right_knee_y_dif

		# Add Lines to Canvas
		self.left_lower_leg = self.canvas.create_line(self.start_left_foot[0],
													  self.start_left_foot[1],
													  left_knee_x,
													  left_knee_y,
													  width=2)
		self.left_upper_leg = self.canvas.create_line(left_knee_x,
													  left_knee_y,
													  self.start_hip[0],
													  self.start_hip[1],
													  width=2)
		self.right_lower_leg = self.canvas.create_line(self.start_right_foot[0],
													   self.start_right_foot[1],
													   right_knee_x,
													   right_knee_y,
													   width=2)
		self.right_upper_leg = self.canvas.create_line(right_knee_x,
													   right_knee_y,
													   self.start_hip[0],
													   self.start_hip[1],
													   width=2)
		self.torso = self.canvas.create_line(self.start_hip[0],
											 self.start_hip[1],
											 self.start_hip[0],
											 self.start_hip[1]-80.0,
											 width=2)

		self.canvas.pack(fill=BOTH, expand=1)

	def left_leg_length_change(self):
		end_hip_dif_x = self.start_left_foot[0] - self.end_hip[0]
		end_hip_dif_y = self.start_left_foot[1] - self.end_hip[1]
		end_hip_angle = math.atan2(end_hip_dif_y, end_hip_dif_x)

		angle_dif = end_hip_angle - self.left_leg_angle
		projection = math.cos(angle_dif)*math.sqrt(end_hip_dif_x**2+end_hip_dif_y**2)

		distance_dif = projection - self.left_leg_length

		iteration_ratio = 1.0/(self.num_iterations - self.current_iteration)

		return self.left_leg_length + distance_dif*iteration_ratio

	def left_leg_angle_change(self):
		end_hip_dif_x = self.start_left_foot[0] - self.end_hip[0]
		end_hip_dif_y = self.start_left_foot[1] - self.end_hip[1]
		end_hip_angle = math.atan2(end_hip_dif_y, end_hip_dif_x)

		angle_dif = end_hip_angle - self.left_leg_angle

		iteration_ratio = 1.0/(self.num_iterations - self.current_iteration)

		return self.left_leg_angle + angle_dif*iteration_ratio

	def right_leg_length_change(self):
		current_hip_x = self.start_left_foot[0] - \
						math.cos(self.left_leg_angle)*self.left_leg_length
		current_hip_y = self.start_left_foot[1] - \
						math.sin(self.left_leg_angle)*self.left_leg_length

		end_right_foot_dif_x = self.end_right_foot[0] - current_hip_x
		end_right_foot_dif_y = self.end_right_foot[1] - current_hip_y
		end_right_foot_angle = math.atan2(end_right_foot_dif_y, end_right_foot_dif_x)

		angle_dif = end_right_foot_angle - self.right_leg_angle
		projection = math.cos(angle_dif)*math.sqrt(end_right_foot_dif_x**2+end_right_foot_dif_y**2)

		distance_dif = projection - self.right_leg_length

		iteration_ratio = 1.0/(self.num_iterations - self.current_iteration)

		return self.right_leg_length + distance_dif*iteration_ratio

	def right_leg_angle_change(self):
		current_hip_x = self.start_left_foot[0] - \
						math.cos(self.left_leg_angle)*self.left_leg_length
		current_hip_y = self.start_left_foot[1] - \
						math.sin(self.left_leg_angle)*self.left_leg_length

		end_right_foot_dif_x = self.end_right_foot[0] - current_hip_x
		end_right_foot_dif_y = self.end_right_foot[1] - current_hip_y
		end_right_foot_angle = math.atan2(end_right_foot_dif_y, end_right_foot_dif_x)

		angle_dif = end_right_foot_angle - self.right_leg_angle

		iteration_ratio = 1.0/(self.num_iterations - self.current_iteration)

		return self.right_leg_angle + angle_dif*iteration_ratio

	def update_variables(self):
		new_left_leg_length = self.left_leg_length_change()
		# print "Old: ", self.left_leg_length, " New: ", new_left_leg_length
		new_left_leg_angle = self.left_leg_angle_change()
		# print "Old: ", self.left_leg_angle, " New: ", new_left_leg_angle
		new_right_leg_length = self.right_leg_length_change()
		# print "Old: ", self.right_leg_length, " New: ", new_right_leg_length
		new_right_leg_angle = self.right_leg_angle_change()
		# print "Old: ", self.right_leg_angle, " New: ", new_right_leg_angle

		self.left_leg_length = new_left_leg_length
		self.left_leg_angle = new_left_leg_angle
		self.right_leg_length = new_right_leg_length
		self.right_leg_angle = new_right_leg_angle

	def animate(self):
		# Calculate Current Position
		left_segment_angle = math.acos((self.left_leg_length/2)/self.segment_length)
		left_knee_x_dif = self.segment_length*math.cos(self.left_leg_angle+left_segment_angle)
		left_knee_y_dif = self.segment_length*math.sin(self.left_leg_angle+left_segment_angle)
		left_knee_x = self.start_left_foot[0]-left_knee_x_dif
		left_knee_y = self.start_left_foot[1]-left_knee_y_dif

		hip_x_dif = self.left_leg_length*math.cos(self.left_leg_angle)
		hip_y_dif = self.left_leg_length*math.sin(self.left_leg_angle)
		hip_x = self.start_left_foot[0]-hip_x_dif
		hip_y = self.start_left_foot[1]-hip_y_dif

		right_segment_angle = math.acos((self.right_leg_length/2)/self.segment_length)
		aligned_angle = self.right_leg_angle - right_segment_angle
		right_knee_x_dif = self.segment_length*math.cos(aligned_angle)
		right_knee_y_dif = self.segment_length*math.sin(aligned_angle)
		right_knee_x = hip_x + right_knee_x_dif
		right_knee_y = hip_y + right_knee_y_dif

		right_foot_x_dif = self.right_leg_length*math.cos(self.right_leg_angle)
		right_foot_y_dif = self.right_leg_length*math.sin(self.right_leg_angle)
		right_foot_x = hip_x + right_foot_x_dif
		right_foot_y = hip_y + right_foot_y_dif

		# Update Lines on Canvas
		self.canvas.coords(self.left_lower_leg, self.start_left_foot[0],
												self.start_left_foot[1],
												left_knee_x,
												left_knee_y)
		self.canvas.coords(self.left_upper_leg, left_knee_x,
												left_knee_y,
												hip_x,
												hip_y)
		self.canvas.coords(self.right_upper_leg, right_knee_x,
												 right_knee_y,
												 hip_x,
												 hip_y)
		self.canvas.coords(self.right_lower_leg, right_foot_x,
												 right_foot_y,
												 right_knee_x,
												 right_knee_y)
		self.canvas.coords(self.torso, hip_x,
									   hip_y,
									   hip_x,
									   hip_y-80.0)

		self.current_iteration = self.current_iteration + 1
		if self.current_iteration < self.num_iterations:
			self.update_variables()
			self.after(10, self.animate)

def main():
	root = Tk()
	ex = ConstraintSolver(root)
	root.geometry("200x250+300+300")
	root.mainloop()

if __name__ == '__main__':
	main()