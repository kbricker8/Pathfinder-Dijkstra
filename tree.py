# Stores values of squares and thier neighbors in the form of a tree as branches are added
class Tree:

	def __init__(self, start):
		self.value = [(start, start)]

	def addBranch(self, child, parent):
		self.value.append( (child, parent) )

		# Finds the shortest path between two given points and 
		# returns the entire path in the form of an array
	def shortestPath(self, start, end):
		path = []
		node = end
		Tree = self.value
		Tree.reverse()
		while node != start:
			for branch in Tree:
				if branch[0] == node:
					path.append(node)
					node = branch[1]
		path.reverse()
		return path