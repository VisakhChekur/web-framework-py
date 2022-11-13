class ControllerNotFound(Exception):
    
    def __init__(self, controller: str):

        self.controller = controller
        super().__init__()

class MethodNotImplemented(Exception):

    def __init__(self, method: str):

        self.method = method
        super().__init__()