from pathlib import Path
from sros2 import _utilities
from cryptography import x509

_KS_ENCLAVES = 'enclaves'
_KS_PUBLIC = 'public'
_KS_PRIVATE = 'private'
_DEFAULT_COMMON_NAME = 'ros2smtCA'


class SMT_ARTIFACT():
    def __init__(self, group_policies, parent_dir='./smt_keystore'):
        self.group_policies = group_policies
        if group_policies == []:
            raise ValueError

        self.parent_dir = Path.cwd().joinpath(parent_dir)
        self.parent_dir.mkdir(parents=True, exist_ok=True)

    def create_group_keystore(self):
        groups = set(self.group_policies.keys())
        exist_group_keystore=set()
        for addr in self.parent_dir.iterdir():
            if addr.is_dir():
                if addr.name in groups:
                    if self.check_keystore_integrality(addr):
                        exist_group_keystore.add(addr.name)
                    else:
                        self.rm_tree(addr)
                else:
                    self.rm_tree(addr)
        dir_to_create = groups-exist_group_keystore
        for dir in dir_to_create:
            self.create_single_keystore(self.parent_dir.joinpath(dir))

    def rm_tree(self,pth):
        for child in pth.glob('*'):
            if child.is_file():
                child.unlink()
            else:
                self.rm_tree(child)
        pth.rmdir()

    def create_single_keystore(self,parent_dir):
        for path in (
            parent_dir,
            parent_dir.joinpath(_KS_PUBLIC),
            parent_dir.joinpath(_KS_PRIVATE),
            parent_dir.joinpath(_KS_ENCLAVES)):
                path.mkdir(parents=True, exist_ok=False)

    def check_keystore_integrality(self,keystore):
        #check dir
        dir_name=set()
        for dir in keystore.iterdir():
            dir_name.add(dir.name)
        for dir in [_KS_ENCLAVES,_KS_PRIVATE,_KS_PUBLIC]:
            if dir not in dir_name:
                return False
        return True





    def main(self):
        print('Hi from smt_artifact.')
        self.create_group_keystore()
        # for path in (
        #     self.parent_dir,
        #     self.parent_dir.joinpath(_KS_PUBLIC),
        #     self.parent_dir.joinpath(_KS_PRIVATE),
        #     self.parent_dir.joinpath(_KS_ENCLAVES)):
        #         path.mkdir(parents=True, exist_ok=True)
        # keystore_ca_cert_path = self.parent_dir.joinpath(_KS_PUBLIC, 'ca.cert.pem')
        # keystore_ca_key_path = self.parent_dir.joinpath(_KS_PRIVATE, 'ca.key.pem')
        # self._create_ca_key_cert(keystore_ca_cert_path,keystore_ca_key_path)

    def _create_ca_key_cert(self, ca_key_out_path, ca_cert_out_path):
        cert, private_key = _utilities.build_key_and_cert(
            x509.Name([x509.NameAttribute(x509.oid.NameOID.COMMON_NAME, _DEFAULT_COMMON_NAME)]),
            ca=True)

        _utilities.write_key(private_key, ca_key_out_path)
        _utilities.write_cert(cert, ca_cert_out_path)


def main():
    policy = {'start': {'members': ['/building_map_server'], 'allowPub': ['/map'], 'allowSub': []}, 
            'middle': {'members': ['/rmf_traffic_schedule_node', '/tinyRobot_state_aggregator', '/readonly', '/teleport_dispenser', '/door', '/gazebo', '/mock_docker', '/caddy_fleet_adapter', '/building_systems_visualizer', '/rmf_lift_supervisor', '/teleport_ingestor','/cleanerBotE_state_aggregator', '/slotcar', '/fleet_state_visualizer', '/rmf_traffic_blockade_node', '/deliveryRobot_fleet_adapter', '/door_supervisor', '/caddy_diff_controller'], 'allowPub': ['/tf', '/odom'], 'allowSub': ['/clock', '/cmd_vel']}, 
            'end': {'members': ['/api_client', '/toggle_floors', '/task_requester'], 'allowPub': [], 'allowSub': ['/clock']}}
    smt_artifact = SMT_ARTIFACT(group_policies=policy)
    smt_artifact.main()


if __name__ == '__main__':
    main()
