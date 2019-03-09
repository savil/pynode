
# base class for exceptions
class PyNodeError(Exception):
    def __init__(self, msg: str):
        self._msg = msg
        super().__init__()

# error caused by the system's dependencies e.g. database not accessible
class SystemBadError(PyNodeError):
    pass

# error caused by programmer logic
class ProgrammerError(PyNodeError):
    pass

# error message that should be made visible to the end-user
class UserError(PyNodeError):
    pass
