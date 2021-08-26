# -*- coding: utf-8 -*-
#####################################
# @author [Rex Yu]
# @email  [jiafish@outlook.com]
# @github https://github.com/Rexyyj
# @date   2021-08-19 08:46:18
# @desc 
####################################
from pathlib import Path
from sros2 import _utilities
from cryptography import x509
from cryptography.hazmat.backends import default_backend as cryptography_backend
from cryptography.hazmat.primitives import serialization
from smt_artifact.managers.dir_manager import Dir_Manager
from smt_artifact.managers.governance_manager import Governance_Manager
from smt_artifact.managers.permission_manager import Permission_Manager
import time
_KS_ENCLAVES = 'enclaves'
_KS_PUBLIC = 'public'
_KS_PRIVATE = 'private'
_DEFAULT_COMMON_NAME = 'ros2smt'


class SMT_ARTIFACT():
    def __init__(self, group_policies, parent_dir='./smt_keystore', use_keycer_in_keystore=None,keystore_mode = "single"):
        self.group_policies = group_policies
        if group_policies == []:
            raise ValueError

        self.parent_dir = Path.cwd().joinpath(parent_dir)
        self.parent_dir.mkdir(parents=True, exist_ok=True)
        self.keystores = []
        self.store2group ={}
        if keystore_mode == "single":
            self.keystores.append("keystore")
            self.store2group["keystore"]= list(set(self.group_policies.keys()))
        else:
            # ToDo add other keystore implementation
            raise Exception("Keystore mode not yet implemented!!")
        # for key in self.group_policies.keys():
        #     self.keystores.append(self.parent_dir.joinpath("./"+key))

        if use_keycer_in_keystore == None:
            self.cer, self.key = _utilities.build_key_and_cert(
                x509.Name([x509.NameAttribute(x509.oid.NameOID.COMMON_NAME, _DEFAULT_COMMON_NAME)]),
                ca=True)
        else:
            self.cer = _utilities.load_cert(self.parent_dir
                                            .joinpath("./"+use_keycer_in_keystore+"/"+_KS_PUBLIC+"/ca.cert.pem"))
            key_path = self.parent_dir.joinpath(
                "./"+use_keycer_in_keystore+"/"+_KS_PRIVATE+"/ca.key.pem")
            with open(key_path, 'rb') as key_file:
                self.key = serialization.load_pem_private_key(key_file.read(), None, cryptography_backend())

        self.dir_manager = Dir_Manager(self.key,self.cer)
        self.governance_manager = Governance_Manager(self.key,self.cer)
        self.permission_manager = Permission_Manager(self.key,self.cer,self.group_policies)


    def main(self):
        # print('Hi from smt_artifact.')
        self.dir_manager.create_group_keystore(self.parent_dir,self.keystores)
        self.governance_manager.create_governances(self.parent_dir,self.keystores)
        self.dir_manager.create_group_permission_dir(self.parent_dir,self.keystores,self.group_policies.keys())
        self.permission_manager.create_permission(self.parent_dir,self.keystores,self.store2group)

    def output_node2pol_map(self):
        with open(self.parent_dir+"/node2enclave.txt","w") as f:
            f.write("Node  ---->  Enclave")
            for key in self.group_policies.keys():
                for node in self.group_policies[key]["members"]:
                    f.write(node+"  ---->  "+key+"\n")



def main():
    policy = {'start': {'members': ['/building_map_server'], 'allowPub': ['/map'], 'allowSub': []},
              'middle': {'members': ['/rmf_traffic_schedule_node', '/tinyRobot_state_aggregator', '/readonly', '/teleport_dispenser', '/door', '/gazebo', '/mock_docker', '/caddy_fleet_adapter', '/building_systems_visualizer', '/rmf_lift_supervisor', '/teleport_ingestor', '/cleanerBotE_state_aggregator', '/slotcar', '/fleet_state_visualizer', '/rmf_traffic_blockade_node', '/deliveryRobot_fleet_adapter', '/door_supervisor', '/caddy_diff_controller'], 'allowPub': ['/tf', '/odom'], 'allowSub': ['/clock', '/cmd_vel']},
              'end': {'members': ['/api_client', '/toggle_floors', '/task_requester'], 'allowPub': [], 'allowSub': ['/clock']}}
    smt_artifact = SMT_ARTIFACT(group_policies=policy)
    smt_artifact.main()
    smt_artifact.output_node2pol_map()


if __name__ == '__main__':
    main()
