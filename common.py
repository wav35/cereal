
class Cereal:
    def __init__(self, kind: str):
        self.kind = kind

    def get_type(self) -> str:
        """
        Gets the type of cereal ("client" or "server")
        """
        return self.kind

