from pathlib import Path
from sros2 import _utilities
from cryptography import x509
from sros2 import keystore
from smt_artifact.managers.dir_manager import DIR_MANAGER

_KS_ENCLAVES = 'enclaves'
_KS_PUBLIC = 'public'
_KS_PRIVATE = 'private'
_DEFAULT_COMMON_NAME = 'ros2smtCA'


class SMT_ARTIFACT():
    def __init__(self, group_policies, parent_dir='./smt_keystore', use_keycer_in_keystore=None):
        self.group_policies = group_policies
        if group_policies == []:
            raise ValueError

        self.parent_dir = Path.cwd().joinpath(parent_dir)
        self.parent_dir.mkdir(parents=True, exist_ok=True)
        self.keystores = []
        for key in self.group_policies.keys():
            self.keystores.append(self.parent_dir.joinpath("./"+key))

        if use_keycer_in_keystore == None:
            self.cer, self.key = _utilities.build_key_and_cert(
                x509.Name([x509.NameAttribute(x509.oid.NameOID.COMMON_NAME, _DEFAULT_COMMON_NAME)]),
                ca=True)
        else:
            self.cer = _utilities.load_cert(self.parent_dir
                                            .joinpath("./"+use_keycer_in_keystore+"/"+_KS_PUBLIC+"/ca.cert.pem"))
            self.key = self.parent_dir.joinpath(
                "./"+use_keycer_in_keystore+"/"+_KS_PRIVATE+"/ca.key.pem").read_text()


    def create_keystore(self):
        dir_manager = DIR_MANAGER(self.key,self.cer)
        dir_manager.create_group_keystore(self.parent_dir,self.keystores)

        



    def main(self):
        print('Hi from smt_artifact.')
        self.create_keystore()




def main():
    policy = {'start': {'members': ['/building_map_server'], 'allowPub': ['/map'], 'allowSub': []},
              'middle': {'members': ['/rmf_traffic_schedule_node', '/tinyRobot_state_aggregator', '/readonly', '/teleport_dispenser', '/door', '/gazebo', '/mock_docker', '/caddy_fleet_adapter', '/building_systems_visualizer', '/rmf_lift_supervisor', '/teleport_ingestor', '/cleanerBotE_state_aggregator', '/slotcar', '/fleet_state_visualizer', '/rmf_traffic_blockade_node', '/deliveryRobot_fleet_adapter', '/door_supervisor', '/caddy_diff_controller'], 'allowPub': ['/tf', '/odom'], 'allowSub': ['/clock', '/cmd_vel']},
              'end': {'members': ['/api_client', '/toggle_floors', '/task_requester'], 'allowPub': [], 'allowSub': ['/clock']}}
    smt_artifact = SMT_ARTIFACT(group_policies=policy,use_keycer_in_keystore="end")
    smt_artifact.main()


if __name__ == '__main__':
    main()
