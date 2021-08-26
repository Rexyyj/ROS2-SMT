# -*- coding: utf-8 -*-
#####################################
# @author [Rex Yu]
# @email  [jiafish@outlook.com]
# @github https://github.com/Rexyyj
# @date   2021-08-19 08:48:53
# @desc 
####################################

from pyspark.sql import SparkSession
from graphframes import GraphFrame
from pyspark import SparkConf
from pyspark import SparkContext
from smt_relationship.analyzers.topic_analyzer import Topic_Analyzer
import sys


class SMT_RELATIONSHIP:

    def __init__(self, from_file=True, ckpt_dir="./ckpt", vertices=[], edges=[],filePath = "./"):
        conf = SparkConf().setAppName("Analyzer")
        conf.set("spark.jars.packages", "graphframes:graphframes:0.8.1-spark3.0-s_2.12")
        conf.set("spark.jars.repositories", "https://repos.spark-packages.org/")
        self.sc = SparkContext(conf=conf)
        self.sc.setCheckpointDir(ckpt_dir)
        self.spark = SparkSession.builder.getOrCreate()

        if from_file == True:
            self.vertices = self.spark.read.load(filePath+"vertices.csv",
                                                 format="csv",
                                                 header=True,
                                                 inferSchema=True,
                                                 sep=',')
            self.edges = self.spark.read.load(filePath+"edges.csv",
                                              format="csv",
                                              header=True,
                                              inferSchema=True,
                                              sep=',')
        else:
            self.vertices = self.spark.createDataFrame(vertices,["id", "name_space", "name", "is_hidden"])
            self.edges = self.spark.createDataFrame(edges, ["src", "dst", "type", "type_name"])
            pass
    #config={"remove_hidden":true,"remove_default":true,"grouping_method":"RBAC","mode":"src-mid-dst"}
    def analysis(self,config):
        v = self.vertices
        e = self.edges.filter("type=='topic'")
        g = GraphFrame(v, e)
        topicAnalyzer = Topic_Analyzer(v, e)
       
        if config["remove_hidden"]=="True":
            topicAnalyzer.remove_all_hidden()
        if config["remove_default"]=="True":
            topicAnalyzer.remove_default_edges()

        topicAnalyzer.create_graph()
        if config["grouping_method"]=="RBAC":
            topicAnalyzer.RBAC_grouping(mode=config["mode"])
        
        return topicAnalyzer.get_group_policy()

            


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
        topicAnalyzer.RBAC_grouping(mode="src-mid-dst")
        print(topicAnalyzer.get_group_policy())


def main():
    print('Hi from smt_relationship.')
    print(sys.version_info)
    rela = SMT_RELATIONSHIP()
    rela.test()


if __name__ == '__main__':
    main()
