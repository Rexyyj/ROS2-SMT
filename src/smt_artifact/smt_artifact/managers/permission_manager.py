# -*- coding: utf-8 -*-
#####################################
# @author [Rex Yu]
# @email  [jiafish@outlook.com]
# @github https://github.com/Rexyyj
# @date   2021-08-19 08:47:42
# @desc 
####################################

from smt_artifact.managers.common_manager import Common_Manager
from datetime import datetime
from xml.dom import minidom
_DEFAULT_POLICY_RQ = ["/describe_parametersRequest",
                      "/get_parameter_typesRequest",
                      "/get_parameter_typesRequest",
                      "/list_parametersRequest",
                      "/set_parametersRequest",
                      "/set_parameters_atomicallyRequest"
                      ]

_DEFAULT_POLICY_RR = ["/describe_parametersReply",
                      "/get_parameter_typesReply",
                      "/get_parametersReply",
                      "/list_parametersReply",
                      "/list_parametersReply",
                      "/set_parameters_atomicallyReply"
                      ]



class Permission_Manager(Common_Manager):
    def __init__(self, key, cer, policies,
                 _KS_ENCLAVES='enclaves',
                 _KS_PUBLIC='public',
                 _KS_PRIVATE='private',
                 _DEFAULT_COMMON_NAME='ros2smt',
                 ) -> None:
        self._KS_ENCLAVES = _KS_ENCLAVES
        self._KS_PUBLIC = _KS_PUBLIC
        self._KS_PRIVATE = _KS_PRIVATE
        self._DEFAULT_COMMON_NAME = _DEFAULT_COMMON_NAME
        self.key = key
        self.cer = cer
        self.policies = policies

    def create_permission(self, parent_dir,keystores,store2group):
        for keystore in keystores:
            for group in store2group[keystore]:
                permission_path = parent_dir.joinpath(keystore).joinpath(self._KS_ENCLAVES).joinpath(group)
                if not self.is_permission_file_exist(permission_path):
                    self.create_single_permission(permission_path.joinpath(
                        "./permissions.p7s"), group)

    def get_valid_time(self):
        now = datetime.now()
        start_time = now.strftime("%Y-%m-%dT%H:%M:%S")
        end_of_valid_year = str(int(now.strftime("%Y"))+10)
        end_time = now.strftime(end_of_valid_year+"-%m-%dT%H:%M:%S")
        return start_time, end_time

    def join_layer(self, doc, parent, name, attribute=[], value=[]):
        layer = doc.createElement(name)
        if len(attribute) > 0:
            for i in range(len(attribute)):
                layer.setAttribute(attribute[i], value[i])
        if parent is not None:
            parent.appendChild(layer)
        else:
            doc.appendChild(layer)
        return layer

    def join_node(self, doc, parent, name, value):
        node = doc.createElement(name)
        val = doc.createTextNode(value)
        node.appendChild(val)
        parent.appendChild(node)
        return node

    def create_basic_structure(self, root, group_name):

        dds = self.join_layer(root, None, "dds", ["xmlns:xsi", "xsi:noNamespaceSchemaLocation"], [
                              "http://www.w3.org/2001/XMLSchema-instance", "http://www.omg.org/spec/DDS-SECURITY/20170901/omg_shared_ca_governance.xsd"])

        permissions = self.join_layer(root, dds, "permissions")

        grant = self.join_layer(root, permissions, "grant", ["name"], [group_name])

        self.join_node(root, grant, "subject_name", "CN="+group_name)
        validity = self.join_layer(root, grant, "validity")
        #allow_rule1 = self.join_layer(root, grant, "start_rule")
        allow_rule2 = self.join_layer(root, grant, "allow_rule")
        self.join_node(root, grant, "default", "DENY")

        start_time, end_time = self.get_valid_time()
        self.join_node(root, validity, "not_before", start_time)
        self.join_node(root, validity, "not_after", end_time)

        domains = self.join_layer(root, allow_rule2, "domains")
        publish = self.join_layer(root, allow_rule2, "publish")
        subscribe = self.join_layer(root, allow_rule2, "subscribe")

        self.join_node(root, domains, "id", "0")

        topicsP = self.join_layer(root, publish, "topics")
        self.join_node(root, topicsP, "topic", "ros_discovery_info")

        topicsS = self.join_layer(root, subscribe, "topics")
        self.join_node(root, topicsS, "topic", "ros_discovery_info")

        return allow_rule2

    def add_permission_policy(self, root, parent, group_name):
        policy = self.policies[group_name]

        domains = self.join_layer(root, parent, "domains")
        publish = self.join_layer(root, parent, "publish")
        subscribe = self.join_layer(root, parent, "subscribe")

        self.join_node(root, domains, "id", "0")

        topicsP = self.join_layer(root, publish, "topics")
        topicsS = self.join_layer(root, subscribe, "topics")
        for member in policy["members"]:
            for default in _DEFAULT_POLICY_RQ:
                self.join_node(root, topicsP, "topic", "rq"+member+default)       
                self.join_node(root, topicsS, "topic", "rq"+member+default)
            for default in _DEFAULT_POLICY_RR:
                self.join_node(root, topicsP, "topic", "rr"+member+default)       
                self.join_node(root, topicsS, "topic", "rr"+member+default)

        self.join_node(root,topicsP,"topic","rt/parameter_events")
        self.join_node(root,topicsS,"topic","rt/parameter_events")
        self.join_node(root,topicsP,"topic","rt/rosout")


        for allow_pub in policy["allowPub"]:
            self.join_node(root,topicsP,"topic","rt"+allow_pub)
        for allow_sub in policy["allowSub"]:
            self.join_node(root,topicsS,"topic","rt"+allow_sub)

    def create_single_permission(self, path, group_name):
        root = minidom.Document()
        permission_parent = self.create_basic_structure(root, group_name)
        self.add_permission_policy(root, permission_parent, group_name)
        
        xml_str = root.toprettyxml(indent="  ")
        with open(path, 'wb') as f:
            f.write(self.sign_bytes(self.cer, self.key, str.encode(xml_str)))
