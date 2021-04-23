from pyspark.sql import SparkSession
from graphframes import GraphFrame
from topic_analyzer import TOPIC_ANALYZER

class SMT_RELATIONSHIP:

	def __init__(self):
		self.spark = SparkSession.builder.getOrCreate()

		



def main():
    print('Hi from smt_relationship.')


if __name__ == '__main__':
    main()
