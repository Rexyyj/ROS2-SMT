from pathlib import Path
from sros2 import _utilities
from cryptography import x509

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

    def create_group_keystore(self):
        exist_group_keystore = set()
        for addr in self.parent_dir.iterdir():
            if addr.is_dir():
                if addr in self.keystores:
                    if self.check_keystore_integrality(addr):
                        exist_group_keystore.add(addr)
                    else:
                        self.rm_tree(addr)
                else:
                    self.rm_tree(addr)
        dir_to_create = set(self.keystores)-exist_group_keystore
        for dir in dir_to_create:
            self.create_single_keystore(self.parent_dir.joinpath(dir))

    def rm_tree(self, pth):
        for child in pth.glob('*'):
            if child.is_file():
                child.unlink()
            else:
                self.rm_tree(child)
        pth.rmdir()

    def create_single_keystore(self, keystore_path):
        for path in (
                keystore_path,
                keystore_path.joinpath(_KS_PUBLIC),
                keystore_path.joinpath(_KS_PRIVATE),
                keystore_path.joinpath(_KS_ENCLAVES)):
            path.mkdir(parents=True, exist_ok=False)

        keystore_ca_cert_path = keystore_path.joinpath(_KS_PUBLIC, 'ca.cert.pem')
        keystore_ca_key_path = keystore_path.joinpath(_KS_PRIVATE, 'ca.key.pem')

        keystore_permissions_ca_cert_path = keystore_path.joinpath(
            _KS_PUBLIC, 'permissions_ca.cert.pem')
        keystore_permissions_ca_key_path = keystore_path.joinpath(
            _KS_PRIVATE, 'permissions_ca.key.pem')

        keystore_identity_ca_cert_path = keystore_path.joinpath(
            _KS_PUBLIC, 'identity_ca.cert.pem')
        keystore_identity_ca_key_path = keystore_path.joinpath(
            _KS_PRIVATE, 'identity_ca.key.pem')

        required_files = (
            keystore_permissions_ca_cert_path,
            keystore_permissions_ca_key_path,
            keystore_identity_ca_cert_path,
            keystore_identity_ca_key_path,
        )
        if not all(x.is_file() for x in required_files):
            _utilities.write_cert(self.cer, keystore_ca_cert_path)
            if isinstance(self.key, str):
                keystore_ca_key_path.write_text(self.key)
            else:
                _utilities.write_key(self.key, keystore_ca_key_path)

        for path in (keystore_permissions_ca_cert_path, keystore_identity_ca_cert_path):
            _utilities.create_symlink(src=Path('ca.cert.pem'), dst=path)

        for path in (keystore_permissions_ca_key_path, keystore_identity_ca_key_path):
            _utilities.create_symlink(src=Path('ca.key.pem'), dst=path)
        

    def check_keystore_integrality(self, keystore):
        # check dir
        dir_name = set()
        for dir in keystore.iterdir():
            dir_name.add(dir.name)
        for dir in [_KS_ENCLAVES, _KS_PRIVATE, _KS_PUBLIC]:
            if dir not in dir_name:
                return False
        return True
        # ToDo: check other layser

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



def main():
    policy = {'start': {'members': ['/building_map_server'], 'allowPub': ['/map'], 'allowSub': []},
              'middle': {'members': ['/rmf_traffic_schedule_node', '/tinyRobot_state_aggregator', '/readonly', '/teleport_dispenser', '/door', '/gazebo', '/mock_docker', '/caddy_fleet_adapter', '/building_systems_visualizer', '/rmf_lift_supervisor', '/teleport_ingestor', '/cleanerBotE_state_aggregator', '/slotcar', '/fleet_state_visualizer', '/rmf_traffic_blockade_node', '/deliveryRobot_fleet_adapter', '/door_supervisor', '/caddy_diff_controller'], 'allowPub': ['/tf', '/odom'], 'allowSub': ['/clock', '/cmd_vel']},
              'end': {'members': ['/api_client', '/toggle_floors', '/task_requester'], 'allowPub': [], 'allowSub': ['/clock']}}
    smt_artifact = SMT_ARTIFACT(group_policies=policy,use_keycer_in_keystore="end")
    smt_artifact.main()


if __name__ == '__main__':
    main()
