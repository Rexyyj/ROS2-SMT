from graphframes import GraphFrame
from smt_relationship.analyzers.analyzer import Analyzer


class Topic_Analyzer(Analyzer):

    def __init__(self, vertices, edges):
        super(Topic_Analyzer, self).__init__(vertices, edges)
        self.group_policy = {}
        # {"group0":{"members":["a","b"],"pub":["topic1","topic2"],"sub":["topic1","topic2"]}}
        pass

    def strongly_connected_grouping(self):
        if self._graph == None:
            raise RuntimeError("Graph undefined...")
        connComp = self._graph.stronglyConnectedComponents(maxIter=100).cache()
        # get group id (component number)
        comps = connComp.select("component").distinct().rdd.map(lambda row: row.component).collect()
        relationFrame = connComp.join(self._edges, connComp.id == self._edges.src)\
            .selectExpr("component", "id", "type_name AS pubTopic")
        relationFrame = relationFrame.join(self._edges, relationFrame.id == self._edges.dst)\
            .selectExpr("component", "id", "pubTopic", "type_name AS subTopic")\
            .rdd.map(lambda row: [row.component, row.id, row.pubTopic, row.subTopic]).collect()
        self.group_policy = {}
        for comp in comps:
            members = set()
            pub = set()
            sub = set()
            for relation in relationFrame:
                if relation[0] == comp:
                    members.add(relation[1])
                    pub.add(relation[2])
                    sub.add(relation[3])
            self.group_policy[comp] = {"members": list(
                members), "allowPub": list(pub), "allowSub": list(sub)}
        # pubFrame = connComp.join(self._edges,connComp.id==self._edge)
        # self._edges.show()

    def find_starting_vertices(self):
        src = set([row.src for row in self._edges.select("src").collect()])
        dst = set([row.dst for row in self._edges.select("dst").collect()])
        result = set({})
        for ver in set([row.id for row in self._vertices.select("id").collect()]):
            if ver in src and ver not in dst:
                result.add(ver)
        return result

    def find_ending_vertices(self):
        pass

    def find_middleware_vertices(self):
        pass

    def get_group_policy(self):
        return self.group_policy
