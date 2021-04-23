from pyspark import SparkConf,SparkContext
from pyspark.sql import SparkSession
from graphframes import GraphFrame
from smt_relationship.analyzers.topic_analyzer import Topic_Analyzer

class SMT_RELATIONSHIP:

	def __init__(self,from_file = True):
		self.spark = SparkSession.builder.getOrCreate()
		if from_file == True:
			self.vertices = self.spark.read.load(  "./vertices.csv",\
												format = "csv",\
												header = True,\
												inferSchema = True,
												sep = ',')
			self.edges = self.spark.read.load(  "./edges.csv",\
												format = "csv",\
												header = True,\
												inferSchema = True,
												sep = ',')
		else:
			# ToDo:
			# Directly get vertices and edges form system
			pass
		
	def test(self):
		topicAnalyzer = Topic_Analyzer(self.vertices,self.edges.filter("type==topic"))
		
		

	

		



def main():
	print('Hi from smt_relationship.')


if __name__ == '__main__':
	main()
