from graphframes import GraphFrame
from pyspark.sql import group
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

    def RBAC_grouping(self, mode="namespace"):
        self.group_policy = {}
        if mode == "namespace":
            keys = [row.name_space for row in self._graph.vertices.select(
                "name_space").distinct().collect()]
            group_num = 0
            for key in keys:
                members = set([row.id for row in self._graph.vertices.filter(
                    "name_space=='"+str(key)+"'").select("id").collect()])
                self.group_policy["group"+str(group_num)] = self.members_to_policy(members)
                group_num += 1
        elif mode == "start-middle-end":
            self.group_policy["start"]=self.members_to_policy(self.find_starting_vertices())
            self.group_policy["middle"]=self.members_to_policy(self.find_middleware_vertices())
            self.group_policy["end"] = self.members_to_policy(self.find_ending_vertices())
        else:
            raise ValueError()

    def members_to_policy(self,members):
        for member in members:
            pub = set([row.type_name for row in self._graph.edges.filter(
                "src=='"+member+"'").select("type_name").collect()])
            sub = set([row.type_name for row in self._graph.edges.filter(
                "dst=='"+member+"'").select("type_name").collect()])
        return {"members": list(members), "allowPub": list(pub), "allowSub": list(sub)}

    def get_group_policy(self):
        return self.group_policy
