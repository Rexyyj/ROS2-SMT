from pyspark.sql import SparkSession
from graphframes import GraphFrame
from pyspark import SparkConf
from pyspark import SparkContext
from smt_relationship.analyzers.topic_analyzer import Topic_Analyzer
import sys


class SMT_RELATIONSHIP:

    def __init__(self, from_file=True, ckpt_dir="./ckpt"):
        conf = SparkConf().setAppName("Analyzer")
        conf.set("spark.jars.packages", "graphframes:graphframes:0.8.1-spark3.0-s_2.12")
        conf.set("spark.jars.repositories", "https://repos.spark-packages.org/")
        self.sc = SparkContext(conf=conf)
        self.sc.setCheckpointDir(ckpt_dir)
        self.spark = SparkSession.builder.getOrCreate()

        if from_file == True:
            self.vertices = self.spark.read.load("./vertices.csv",
                                                 format="csv",
                                                 header=True,
                                                 inferSchema=True,
                                                 sep=',')
            self.edges = self.spark.read.load("./edges.csv",
                                              format="csv",
                                              header=True,
                                              inferSchema=True,
                                              sep=',')
        else:
            # ToDo:
            # Directly get vertices and edges form system
            pass

    def test(self):
        v = self.vertices
        e = self.edges.filter("type=='topic'")
        g = GraphFrame(v, e)
        print(g.vertices.count())
        print(g.edges.count())
        topicAnalyzer = Topic_Analyzer(v, e)
        topicAnalyzer.remove_all_hidden()
        topicAnalyzer.remove_default_edges()
        topicAnalyzer.create_graph()
        g = topicAnalyzer.get_graph()
        print(g.vertices.count())
        print(g.edges.count())
        topicAnalyzer.RBAC_grouping(mode="start-middle-end")
        print(topicAnalyzer.get_group_policy())


def main():
    print('Hi from smt_relationship.')
    print(sys.version_info)
    rela = SMT_RELATIONSHIP()
    rela.test()


if __name__ == '__main__':
    main()
