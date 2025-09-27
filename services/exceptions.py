class ProtocoloDuplicadoException(Exception):
    """Exceção para indicar que o protocolo já existe."""
    def __init__(self, message="O protocolo já está em uso."):
        self.message = message
        super().__init__(self.message)


