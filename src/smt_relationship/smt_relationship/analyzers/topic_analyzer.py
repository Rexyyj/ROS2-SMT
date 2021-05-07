from graphframes import GraphFrame
from smt_relationship.analyzers.analyzer import Analyzer

class Topic_Analyzer(Analyzer):

	def __init__(self,vertices,edges,spark):
		super(Topic_Analyzer,self).__init__(vertices,edges)
		
		pass