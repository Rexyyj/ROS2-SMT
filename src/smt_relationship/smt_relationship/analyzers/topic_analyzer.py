from graphframes import GraphFrame
from smt_relationship.analyzers.analyzer import Analyzer

class Topic_Analyzer(Analyzer):

	def __init__(self,vertices,edges):
		super(Topic_Analyzer,self).__init__(vertices,edges)
		pass

	def connected_group(self):
		if self._graph == None:
			raise RuntimeError("Graph undefined...")
		connComp=self._graph.stronglyConnectedComponents(maxIter=100)
		connComp.orderBy("component").show()
		nComp = connComp.select("component").distinct().count()
		print("Num of groups: "+str(nComp))

	def find_starting_vertices(self):
		src = set([row.src for row in self._edges.select("src").collect()])
		dst = set([row.dst for row in self._edges.select("dst").collect()])
		result = set({})
		for ver in set([row.id for row in self._vertices.select("id").collect()]):
			if ver in src and ver not in dst:
				result.add(ver)
		return result
	
	def find_ending_vertices(self):
		pass

	def find_middleware_vertices(self):
		pass
