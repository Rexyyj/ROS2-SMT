# -*- coding: utf-8 -*-
#####################################
# @author [Rex Yu]
# @email  [jiafish@outlook.com]
# @github https://github.com/Rexyyj
# @date   2021-08-19 08:47:24
# @desc 
####################################

from sros2 import _utilities
from pathlib import Path
from smt_artifact.managers.common_manager import Common_Manager
from cryptography import x509
from cryptography.hazmat.backends import default_backend as cryptography_backend
from cryptography.hazmat.primitives import serialization

class Dir_Manager(Common_Manager):
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
        

    def create_group_keystore(self, parent_dir, keystores):
        exist_group_keystore = set()
        
        for addr in parent_dir.iterdir():
            if addr.is_dir():
                if addr in keystores:
                    if self.check_keystore_integrality(addr):
                        exist_group_keystore.add(addr)
                    else:
                        self.rm_tree(addr)
                else:
                    self.rm_tree(addr)
        dir_to_create = set(keystores)-exist_group_keystore
        for dir in dir_to_create:
            self.create_single_keystore(parent_dir.joinpath(dir))
    # Todo: Modify the checking procedure
    def create_group_permission_dir(self, parent_dir,keystores, groups):
        for keystore in keystores:
            for group in set(groups):
                self.create_permission_dir(parent_dir.joinpath(keystore),group)

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
                keystore_path.joinpath(self._KS_PUBLIC),
                keystore_path.joinpath(self._KS_PRIVATE),
                keystore_path.joinpath(self._KS_ENCLAVES)):
            path.mkdir(parents=True, exist_ok=False)

        keystore_ca_cert_path = keystore_path.joinpath(self._KS_PUBLIC, 'ca.cert.pem')
        keystore_ca_key_path = keystore_path.joinpath(self._KS_PRIVATE, 'ca.key.pem')

        keystore_permissions_ca_cert_path = keystore_path.joinpath(
            self._KS_PUBLIC, 'permissions_ca.cert.pem')
        keystore_permissions_ca_key_path = keystore_path.joinpath(
            self._KS_PRIVATE, 'permissions_ca.key.pem')

        keystore_identity_ca_cert_path = keystore_path.joinpath(
            self._KS_PUBLIC, 'identity_ca.cert.pem')
        keystore_identity_ca_key_path = keystore_path.joinpath(
            self._KS_PRIVATE, 'identity_ca.key.pem')

        required_files = (
            keystore_permissions_ca_cert_path,
            keystore_permissions_ca_key_path,
            keystore_identity_ca_cert_path,
            keystore_identity_ca_key_path,
        )
        if not all(x.is_file() for x in required_files):
            _utilities.write_cert(self.cer, keystore_ca_cert_path)
            _utilities.write_key(self.key, keystore_ca_key_path)

        for path in (keystore_permissions_ca_cert_path, keystore_identity_ca_cert_path):
            _utilities.create_symlink(src=Path('ca.cert.pem'), dst=path)

        for path in (keystore_permissions_ca_key_path, keystore_identity_ca_key_path):
            _utilities.create_symlink(src=Path('ca.key.pem'), dst=path)

    def create_permission_dir(self,keystore_path,group):
        permission_dir = keystore_path.joinpath(self._KS_ENCLAVES,group)
        permission_dir.mkdir(parents=True, exist_ok=True)
        _utilities.create_symlink(src=Path("../governance.p7s"),dst=permission_dir.joinpath("governance.p7s"))
        _utilities.create_symlink(src=Path("../../public/identity_ca.cert.pem"),dst=permission_dir.joinpath("identity_ca.cert.pem"))
        _utilities.create_symlink(src=Path("../../public/permissions_ca.cert.pem"),dst=permission_dir.joinpath("permissions_ca.cert.pem"))

        # create cert.pem and key.pem
        cert_path = permission_dir.joinpath('cert.pem')
        key_path = permission_dir.joinpath('key.pem')

        cert, private_key = _utilities.build_key_and_cert(
            x509.Name([x509.NameAttribute(x509.oid.NameOID.COMMON_NAME,  u'cryptography.io')]),
            issuer_name=self.cer.subject,
            ca_key=self.key)

        _utilities.write_key(private_key, key_path)
        _utilities.write_cert(cert, cert_path)

