from pytezos.sandbox.node import _SandboxedNodeTestCase


class SandboxedNodeTestCase(_SandboxedNodeTestCase):
    def test_activate_protocol(self) -> None:
        # Arrange
        client = self.get_client().using(key='dictator')

        # Act
        client.activate_protocol('PtEdo2Zk').fill().sign().inject()

        # Assert
        block = client.shell.block()
        self.assertIsNotNone(block['header'].get('content'))
