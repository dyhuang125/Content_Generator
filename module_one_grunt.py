#!/usr/bin/python
import module_one_actor_states as states


# Finds and attacks nearby enemies

class Grunt(Agent):
	# States:
	__NEUTRAL = 0

	def action():
		if state == states.NEUTRAL:
			# Find target
