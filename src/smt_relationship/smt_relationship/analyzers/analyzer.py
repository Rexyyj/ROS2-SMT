from graphframes import GraphFrame, graphframe
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

    def find_source_vertices(self):
        src = set([row.src for row in self._graph.edges.select("src").collect()])
        dst = set([row.dst for row in self._graph.edges.select("dst").collect()])
        result = set({})
        for ver in set([row.id for row in self._graph.vertices.select("id").collect()]):
            if ver in src and ver not in dst:
                result.add(ver)
        return result

    def find_destination_vertices(self):
        src = set([row.src for row in self._graph.edges.select("src").collect()])
        dst = set([row.dst for row in self._graph.edges.select("dst").collect()])
        result = set({})
        for ver in set([row.id for row in self._graph.vertices.select("id").collect()]):
            if ver in dst and ver not in src:
                result.add(ver)
        return result

    def find_middleware_vertices(self):
        starting = self.find_source_vertices()
        ending = self.find_destination_vertices()
        return (set([row.id for row in self._graph.vertices.select("id").collect()])-starting-ending)
