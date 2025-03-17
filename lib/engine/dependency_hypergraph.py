
from collections import deque



class DependencyHypergraphLoopError(Exception):

	__slots__ = ("looping_hyperedges")

	def __init__(self, looping_hyperedges):
		super().__init__()
		self.looping_hyperedges = looping_hyperedges



class DependencyHypergraph():
	"""The dependency graph of rules is a directed hypergraph.
	
	A hypergraph is a graph where the edges are subsets of the set of vertice.
	A directed hypergraph is a hypergraph where each edge is a pair of subsets of
	the set of vertice: the subset of incoming vertice, the subset of outgoing vertice.

	Here, each rule is by definition a directed hyperedge and the set of vertice
	is the union of the set of targets and the set of prerequisites.

	Each rule contains by definition its set of incoming vertice and its set of
	outgoing vertice.
	The other data structures needed to optimize the calculations on the dependency
	hypergraph are:
	- the set of rules for which a given vertice is a prerequisite,
	- the set of rules for which a given vertice is a target.
	"""

	__slots__ = (
		"hyperedges", "vertice",
		"topological_ordering_of_hyperedges",
		"vertice_to_rules_where_prerequisite", "vertice_to_rules_where_target"
	)


	def __init__(self):
		self.hyperedges = set()
		self.vertice = set()
		self.vertice_to_rules_where_prerequisite = {}
		self.vertice_to_rules_where_target = {}


	def add_rule(self, rule):
		self.hyperedges.add(rule)

		if rule.targets is not None:
			for t in rule.targets:
				self.vertice.add(t)
				self.vertice_to_rules_where_target[t] = rule

		if rule.prerequisites is not None:
			for p in rule.prerequisites:
				self.vertice.add(p)
				if p not in self.vertice_to_rules_where_prerequisite:
					self.vertice_to_rules_where_prerequisite[p] = set()
				self.vertice_to_rules_where_prerequisite[p].add(rule)


	def build_topological_ordering_of_hyperedges(self):
		"""This algorithm adapts to directed hypergraphs the algorithm for
		calculating a topological sorting of the vertice of a directed graph,
		and for detecting any loop at the same time.

		This algorithm calculates a topological ordering of the hyperedges of
		the hypergraph and detects any loop.

		The presence of a loop raises an error since it is impossible to generate
		a target which depends on itself, directly or indirectly.
		"""

		# Initialize the arrays of incoming arity of vertice and hyperedge.
		incoming_arity_vertice = {}
		for v in self.vertice:
			incoming_arity_vertice[v] = 1 if v in self.vertice_to_rules_where_target else 0
		
		incoming_arity_hyperedges = {}
		for e in self.hyperedges:
			incoming_arity_hyperedges[e] = len(e.prerequisites) if e.prerequisites is not None else 0
		
		# Queue the vertice with no incoming hyperedges.
		queue_vertice_0_incoming = deque()
		for v in incoming_arity_vertice:
			if incoming_arity_vertice[v] == 0:
				queue_vertice_0_incoming.append(v)
		
		# Queue the hyperedges with no incoming vertice.
		queue_hyperedge_0_incoming = deque()
		for e in incoming_arity_hyperedges:
			if incoming_arity_hyperedges[e] == 0:
				queue_hyperedge_0_incoming.append(e)
		
		topological_ordering = deque()
		
		while len(queue_vertice_0_incoming) != 0 or len(queue_hyperedge_0_incoming) != 0:
			if len(queue_vertice_0_incoming) != 0:
				v = queue_vertice_0_incoming.popleft()
				# v has no incoming hyperedge.
				# v is good for removal from the arity counting of the hyperedges
				# for whom v is an incoming vertice.
				if v in self.vertice_to_rules_where_prerequisite:
					for e in self.vertice_to_rules_where_prerequisite[v]:
						incoming_arity_hyperedges[e] -= 1
						if incoming_arity_hyperedges[e] == 0:
							# e has no incoming vertice anymore, it will be treated.
							queue_hyperedge_0_incoming.append(e)

			elif len(queue_hyperedge_0_incoming) != 0:
				# A pass of the while loop either tackle a vertex or an hyperedge, never both.

				e = queue_hyperedge_0_incoming.popleft()
				# e has no incoming vertice.
				# e is good to be added to the topological ordering.
				# e is good for removal from the arity counting of the vertice
				# for whom e is an incoming hyerpedge.
				topological_ordering.append(e)
				if e.targets is not None:
					for v in e.targets:
						incoming_arity_vertice[v] -= 1
						if incoming_arity_vertice[v] == 0:
							# v has no incoming hyperedge anymore, it will be treated.
							queue_vertice_0_incoming.append(v)
		
		# If there is a loop,
		# the connections between the vertice and hyperedges in that loop never bring a decrement,
		# thus these vertice and hyperedges never appear in the queues,
		# and they remain outside of the topological ordering.
		if len(topological_ordering) != len(self.hyperedges):
			looping_hyperedges = self.hyperedges.difference(topological_ordering)
			raise DependencyHypergraphLoopError(looping_hyperedges)

		self.topological_ordering_of_hyperedges = list(topological_ordering)

