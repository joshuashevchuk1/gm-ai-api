class Config:
    def __init__(self):
        self.base_host = "localhost"
        self.base_port = "8080"
        self.ai_port = int(8020)


    def get_ai_port(self):
        return self.ai_port

    def get_base_host(self):
        return self.base_host

    def get_base_port(self):
        return self.base_port
