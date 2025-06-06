class Config:
    def __init__(self):
        self.base_host = "localhost"
        self.base_port = "8080"


    def get_base_host(self):
        return self.base_host

    def get_base_port(self):
        return self.base_port
