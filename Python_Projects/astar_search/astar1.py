# ASTAR SEARCH ALGORITHM
# COREY WARREN II

# CSE STUDENT RESOURCES, Repository
# DEMONSTRATION CODE
# JUNE 2021

# VIDEO GUIDE used:
# https://www.youtube.com/watch?v=ob4faIum4kQ

# !usr/bin/env python
# /\ above line  is used for Unix-based machines (Mac/Linux)


#//////////////////////////////
#//////////CODE BEGIN//////////
#//////////////////////////////


from queue import PriorityQueue

# Priority Queue is based on Priority we can set.
# Also can be a dictionary of lists, for example.


class State(object):
	def __init__(self, value, parent, start = 0, goal = 0):
		self.children 	= []
		self.parent 	= parent
		self.value		= value
		self.dist		= 0 	# 0 is just a placeholder value here
		if parent:
			self.path 	= parent.path[:] 	# -> Copy parent's path to our path, 'colon'
											# here copies parent list into our list 
											#properly, without us affecting parent.path
											# itself whenever we change the values of
											# self.path.
			self.path.append(value)			# -> Store our own 'value' into path
											# this allows the path continue to be
											# built over time.
			self.start 	= parent.start
			self.goal 	= parent.goal
		else:
			self.path 	= [value]
			self.start 	= start
			self.goal	= goal


	#these two are not defined in the main class,
	#but in the sub-class down below...
	def GetDist(self):
		pass
	def CreateChildren(self):
		pass
    

class State_String(State):
	def __init__(self, value, parent, start = 0, goal =0):

		super(State_String, self).__init__(value, parent, start, goal)

		self.dist = self.GetDist() 			# -> Overrides default value
											# for 'dist' distance value.	
											# ... This function is used to measure
											# the distance from our goal.
	def GetDist(self):
		if self.value == self.goal:			# -> "Goal reached?"
			return 0
		dist = 0
		for i in range(len(self.goal)):
			letter = self.goal[i]			# -> Each letter has a goal place to get
											# to in the string.

			dist += abs(i - self.value.index(letter))
											# /\ -> This gives us the distance
											# that the letter is from its 'target'

		return dist 						# ...This is distance is stored in self.dist 
											# AKA 'dist'.

	def CreateChildren(self):
		if not self.children: 				# -> Extra precaution to ensure we do not
											# make children twice.
			for i in range(len(self.goal)-1):
				val = self.value
				val = val[:i] + val[i+1] + val[i] + val[i+2:] 	
											# -> Switch letter positions.
											# for every pair of letters.
											# ...We are effectively finding every
											# single possible combination of letters
											# from this state.
				child = State_String(val,self)
				self.children.append(child)
			

class AStar_Solver:
	def __init__(self, start, goal):
		self.path = []					# -> Stores problem's solution.
										# as well as the exact sequence to get there.

		self.visitedQueue = []			# -> Keeps track of all children visited.
										# this is so we don't get caught looping over
										# values we've already discovered.
		self.priorityQueue = PriorityQueue()
		self.start = start
		self.goal = goal

	def Solve(self):
		startState = State_String(self.start, 0, self.start, self.goal)

		count = 0 	# < we add one every time we create a child
					# this allows us to identify which child is which

		self.priorityQueue.put( (0, count, startState) )

					# /\ the 0 is the priority number
					# startState is created above, it holds all our states
					# By the way, this (.,.,.) is known as a tuple!
					# A tuple holds multiple items in one variable.

		#This 'while' loop is where solutions are calculated:
		while(not self.path and self.priorityQueue.qsize()):
					# /\ in the above, this just means:
					# while 'my path' is empty
					# and while 'my pQueue' has ANY size at all,
					# continue thru the while loop.

			closestChild = self.priorityQueue.get()[2]
			print(count, '.', end = '')
				# /\ -> Get the first item in the queue,
				# then specifically grab the '2' index item for later use.
				# ...Recall that in the "2" slot 
				# is all of our states in "startState"

			closestChild.CreateChildren()

			self.visitedQueue.append(closestChild.value)

			for child in closestChild.children:
				if child.value not in self.visitedQueue:
					count += 1
					if not child.dist:		# -> AKA "if distance from soln. is 0"
						self.path = child.path
						# /\ if the above is true,
						# this simply means we found our solution!
						break

					self.priorityQueue.put((child.dist,count,child))
						# /\ if above happens, that means we haven't found soln. yet.
						# So, for this 'child' in the closest children prio. queue,
						# have it added to our main prio. queue, keeping track
						# of its distance, which will be used to order
						# the queue during the search for an answer.

		if not self.path:
			print ("Goal of " + self.goal + "is not possible!")
			# /\ -> This means that: 1) no more children exist and
			# 2) we have not found a solution. So the solution is
			# not even possible because there cannot be one.

		return self.path

if __name__ == "__main__":

	# \/ -> Below, our start state and goal state are defined.

	# *NOTE: When customizing your start and goal states,
	# 	realize that getting even up to 11 characters can
	# 	take HUNDREDS OF THOUSANDS of iterations to get
	#	to a solution. This is because there are SO MANY
	#	possible letter combinations on the way to the
	#	solution.*
	# Further reading on the math behind this:
	# https://www.free-online-calculator-use.com/combination-calculator.html

	start 	= "jihgfedcba"
	goal 	= "abcdefghij"

	print ('Starting...')

	a = AStar_Solver(start, goal)		# -> We start at "start" and our target
										# is "goal".
										# ... "a" is now an object of the AStar_Solver
										# class type.

	a.Solve()							# -> Run the solve function.

	for i in range(len(a.path)):
		print("%d) " %i + a.path[i])

