# -*- coding: utf-8 -*-
#####################################
# @author [Rex Yu]
# @email  [jiafish@outlook.com]
# @github https://github.com/Rexyyj
# @date   2021-08-19 08:47:12
# @desc 
####################################
from cryptography.hazmat.bindings.openssl.binding import Binding as SSLBinding

class Common_Manager():
    def __init__(self, _KS_ENCLAVES='enclaves',
                 _KS_PUBLIC='public',
                 _KS_PRIVATE='private',
                 _DEFAULT_COMMON_NAME='ros2smt') -> None:
        self._KS_ENCLAVES = _KS_ENCLAVES
        self._KS_PUBLIC = _KS_PUBLIC
        self._KS_PRIVATE = _KS_PRIVATE
        self._DEFAULT_COMMON_NAME = _DEFAULT_COMMON_NAME

    def check_keystore_integrality(self, keystore):
        # check dir
        dir_name = set()
        for dir in keystore.iterdir():
            dir_name.add(dir.name)
        for dir in [self._KS_ENCLAVES, self._KS_PRIVATE, self._KS_PUBLIC]:
            if dir not in dir_name:
                return False
        return True
        # check key and certificate

        # ToDo: check other layser

    def is_governance_file_exist(self, dir):
        for item in dir.iterdir():
            if item.is_file():
                if item.name == "governance.p7s":
                    return True

        return False
    
    def is_permission_file_exist(self, dir):
        for item in dir.iterdir():
            if item.is_file():
                if item.name == "permission.p7s":
                    return True

        return False

    def sign_bytes(self,cert, key, byte_string):
        # Using two flags here to get the output required:
        #   - PKCS7_DETACHED: Use cleartext signing
        #   - PKCS7_TEXT: Set the MIME headers for text/plain
        flags = SSLBinding.lib.PKCS7_DETACHED
        flags |= SSLBinding.lib.PKCS7_TEXT

        # Convert the byte string into a buffer for SSL
        bio_in = SSLBinding.lib.BIO_new_mem_buf(byte_string, len(byte_string))
        try:
            pkcs7 = SSLBinding.lib.PKCS7_sign(
                cert._x509, key._evp_pkey, SSLBinding.ffi.NULL, bio_in, flags)
        finally:
            # Free the memory allocated for the buffer
            SSLBinding.lib.BIO_free(bio_in)

        # PKCS7_sign consumes the buffer; allocate a new one again to get it into the final document
        bio_in = SSLBinding.lib.BIO_new_mem_buf(byte_string, len(byte_string))
        try:
            # Allocate a buffer for the output document
            bio_out = SSLBinding.lib.BIO_new(SSLBinding.lib.BIO_s_mem())
            try:
                # Write the final document out to the buffer
                SSLBinding.lib.SMIME_write_PKCS7(bio_out, pkcs7, bio_in, flags)

                # Copy the output document back to python-managed memory
                result_buffer = SSLBinding.ffi.new('char**')
                buffer_length = SSLBinding.lib.BIO_get_mem_data(bio_out, result_buffer)
                output = SSLBinding.ffi.buffer(result_buffer[0], buffer_length)[:]
            finally:
                # Free the memory required for the output buffer
                SSLBinding.lib.BIO_free(bio_out)
        finally:
            # Free the memory allocated for the input buffer
            SSLBinding.lib.BIO_free(bio_in)

        return output
