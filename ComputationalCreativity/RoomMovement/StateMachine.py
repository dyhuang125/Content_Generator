class StateMachine():
	def __init__(self, StateSpace, StartState):
		self.stateSpace = StateSpace
		self.startState = StartState

	def debug_print(self):
		print self.stateSpace
		print self.startState

def main():
	sm = StateMachine(1, 2)
	sm.debug_print()

if __name__ == '__main__':
	main()
