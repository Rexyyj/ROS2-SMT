from graphframes import GraphFrame
from smt_relationship.analyzers.analyzer import Analyzer

class Topic_Analyzer(Analyzer):

	def __init__(self,vertices,edges):
		super(Topic_Analyzer,self).__init__(vertices,edges)
		pass

	def connected_group(self):
		connComp=self._graph.stronglyConnectedComponents(maxIter=10)
		connComp.orderBy("component").show()
		nComp = connComp.select("component").distinct().count()
		print("Num of groups: "+str(nComp))