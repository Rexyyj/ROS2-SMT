from pyspark.sql import SparkSession
from graphframes import GraphFrame
from analyzer import Analyzer

class Topic_Analyzer(Analyzer):

	def __init__(self,vertices,edges):
		super(Topic_Analyzer,self).__init__(vertices,edges)
		pass