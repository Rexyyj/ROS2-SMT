from graphframes import GraphFrame
from pyspark.sql import SparkSession

DEFAULT_EDGES = {"parameter_events", "rosout", "describe_parameters",
                 "get_parameter_types", "get_parameters", "list_parameters",
                                        "set_parameters", "set_parameters_atomically"}


class Analyzer(object):

    def __init__(self, vertices, edges):
        self.spark = SparkSession.builder.getOrCreate()
        self._vertices = vertices
        self._edges = edges
        self._graph = None

        self.define_udf()

    def define_udf(self):
        self.spark.udf.register("is_hidden", lambda name: any(
            part.startswith("_") for part in name.split('/')))
        self.spark.udf.register("is_default", lambda edge: any(
            part in DEFAULT_EDGES for part in edge.split('/')))

    def remove_hidden_vertices(self):
        if self._graph != None:
            raise RuntimeError("Graph already fixed...")
        self._vertices = self._vertices.filter("is_hidden =='False'")

    def remove_hidden_edges(self):
        if self._graph != None:
            raise RuntimeError("Graph already fixed...")
        self._edges = self._edges.filter("is_hidden(src)==False and \
                                        is_hidden(dst)==False and \
                                        is_hidden(type_name)==False")

    def remove_all_hidden(self):
        if self._graph != None:
            raise RuntimeError("Graph already fixed...")
        self.remove_hidden_edges()
        self.remove_hidden_vertices()

    def remove_default_edges(self):
        if self._graph != None:
            raise RuntimeError("Graph already fixed...")
        self._edges = self._edges.filter("is_default(type_name)==False")

    def create_graph(self, drop=False):
        v = self._vertices
        e = self._edges
        if self._graph == None:
            if drop == True:
                self._graph = GraphFrame(v, e).dropIsolatedVertices()
            else:
                self._graph = GraphFrame(v, e)
        else:
            raise ValueError("Redefine graph in a Analyzer")

    def get_graph(self):
        return self._graph
