from pyspark import SparkConf,SparkContext
from pyspark.sql import SparkSession
from graphframes import GraphFrame

class Analyzer(object):
	
	def __init__(self,vertices,edges,ckpt_dir = "./ckpt_dir"):
		conf = SparkConf().setAppName("Analyzer")
		self.sc = SparkContext(conf=conf)
		self.sc.setCheckpointDir(ckpt_dir)
		self.spark = SparkSession.builder.getOrCreate()
		self.spark.udf.register("is_hidden",self._is_hidden_name)

		self._vertices =vertices
		self._edges = edges
		self._graph = None

	def _is_hidden_name(self,name):
		# note, we're assuming the hidden node prefix is the same for other hidden names
		return any(part.startswith("_") for part in name.split('/'))

	def remove_hidden_vertices(self):
		self._vertices = self._vertices.filter("is_hidden == False")

	def remove_hidden_edges(self):
		self._edges = self._edges.filter("is_hidden(src)==False and \
										is_hidden(dst)==False and \
										is_hidden(type_name)==False")

	def remove_all_hidden(self):
		self.remove_hidden_edges()
		self.remove_hidden_vertices()

	def create_graph(self,drop=False):
		if self._graph == None:
			if drop == True:
				self._graph = GraphFrame(self._vertices,self._edges).dropIsolatedVertices()
			else:
				self._graph = GraphFrame(self._vertices,self._edges)
		else:
			raise ValueError("Redefine graph in a Analyzer")


	def get_graph(self):
		return self._graph