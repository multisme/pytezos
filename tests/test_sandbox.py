from pytezos.sandbox.node import _SandboxedNodeTestCase


class SandboxedNodeTestCase(_SandboxedNodeTestCase):
    def test_activate_protocol(self):
        self.activate_protocol()

    # def test_transfer(self) -> None:
    #     # Arrange
    #     client = self.get_client()
    #     client.shell.block()
    #     operation = client.transaction(destination='tz1gjaF81ZRRvdzjobyfVNsAeSC6PScjfQwN', amount=42)

    #     # Act
    #     operation.autofill().sign().inject()

    #     # Assert
