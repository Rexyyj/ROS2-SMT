
class CHECK_MANAGER():
    def __init__(self, _KS_ENCLAVES='enclaves',
                 _KS_PUBLIC='public',
                 _KS_PRIVATE='private',
                 _DEFAULT_COMMON_NAME='ros2smtCA') -> None:
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
