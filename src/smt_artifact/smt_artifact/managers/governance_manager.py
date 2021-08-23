# -*- coding: utf-8 -*-
#####################################
# @author [Rex Yu]
# @email  [jiafish@outlook.com]
# @github https://github.com/Rexyyj
# @date   2021-08-19 08:47:32
# @desc 
####################################

from smt_artifact.managers.common_manager import Common_Manager
import lxml
import sros2.errors
from sros2.policy import get_transport_default, get_transport_schema
from xml.dom import minidom


class Governance_Manager(Common_Manager):
    def __init__(self, key, cer,
                 _KS_ENCLAVES='enclaves',
                 _KS_PUBLIC='public',
                 _KS_PRIVATE='private',
                 _DEFAULT_COMMON_NAME='/C=NL/ST=OV/L=Locality Name/OU=Example OU/O=Example ID CA Organization/CN=Example ID CA/emailAddress=authority@cycloneddssecurity.adlinktech.com',
                 ) -> None:
        self._KS_ENCLAVES = _KS_ENCLAVES
        self._KS_PUBLIC = _KS_PUBLIC
        self._KS_PRIVATE = _KS_PRIVATE
        self._DEFAULT_COMMON_NAME = _DEFAULT_COMMON_NAME
        self.key = key
        self.cer = cer

    def create_governances(self, parent_dir,keystores):
        for keystore in keystores:
            enclaves_path = parent_dir.joinpath(keystore).joinpath(self._KS_ENCLAVES)
            if not self.is_governance_file_exist(enclaves_path):
                self.create_single_governance(enclaves_path.joinpath("./governance.p7s"))

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

    def create_single_governance(self, path):
        root = minidom.Document()

        dds = self.join_layer(root, None, "dds", ["xmlns:xsi", "xsi:noNamespaceSchemaLocation"], [
                              "http://www.w3.org/2001/XMLSchema-instance", "http://www.omg.org/spec/DDS-SECURITY/20170901/omg_shared_ca_governance.xsd"])
        domain_access_rules = self.join_layer(root, dds, "domain_access_rules")
        domain_rule = self.join_layer(root, domain_access_rules, "domain_rule")

        domains = self.join_layer(root, domain_rule, "domains")
        topic_access_rules = self.join_layer(root, domain_rule, "topic_access_rules")
        allow_unauthenticated_participants = self.join_node(
            root, domain_rule, "allow_unauthenticated_participants", "false")
        enable_join_access_control = self.join_node(
            root, domain_rule, "enable_join_access_control", "true")
        discovery_protection_kind = self.join_node(
            root, domain_rule, "discovery_protection_kind", "ENCRYPT")
        liveliness_protection_kind = self.join_node(
            root, domain_rule, "liveliness_protection_kind", "ENCRYPT")
        rtps_protection_kind = self.join_node(root, domain_rule, "rtps_protection_kind", "SIGN")

        id = self.join_node(root, domains, "id", "0")
        topic_rule = self.join_layer(root, topic_access_rules, "topic_rule")

        topic_expression = self.join_node(root, topic_rule, "topic_expression", "*")
        enable_discovery_protection = self.join_node(
            root, topic_rule, "enable_discovery_protection", "true")
        enable_liveliness_protection = self.join_node(
            root, topic_rule, "enable_liveliness_protection", "true")
        enable_read_access_control = self.join_node(
            root, topic_rule, "enable_read_access_control", "true")
        enable_write_access_control = self.join_node(
            root, topic_rule, "enable_write_access_control", "true")
        metadata_protection_kind = self.join_node(
            root, topic_rule, "metadata_protection_kind", "ENCRYPT")
        data_protection_kind = self.join_node(root, topic_rule, "data_protection_kind", "ENCRYPT")

        xml_str = root.toprettyxml(indent="\t")
        with open(path, 'wb') as f:
            f.write(self.sign_bytes(self.cer, self.key, str.encode(xml_str)))
