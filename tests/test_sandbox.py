import logging
from pytezos.logging import logger
from pprint import pprint
from time import sleep
from pytezos.client import PyTezosClient
from pytezos.sandbox.node import _SandboxedNodeTestCase
from pytezos.sandbox.parameters import sandbox_params, sandbox_addresses, sandbox_protocols

logger.setLevel(logging.DEBUG)

# NOTE: Node won't be wiped between tests so alphabetical order of method names matters
class SandboxedNodeTestCase(_SandboxedNodeTestCase):
    def test_1_activate_protocol(self) -> None:
        # Arrange
        client = self.get_client().using(key='dictator')

        # Act
        op = client.activate_protocol('PtEdo2Zk')
        op.fill().sign().inject()

        # Assert
        block = client.shell.block()
        self.assertIsNotNone(block['header'].get('content'))

    def test_2_bake_empty_block(self) -> None:
        # Arrange
        client = self.get_client().using(key='edsk3gUfUPyBSfrS9CCgmCiQsTCHGkviBDusMxDJstFtojtc1zcpsh')

        # Act
        op = client.bake_block()
        # FIXME: proto.008-PtEdo2Zk.operation.not_enough_endorsements_for_priority
        op.fill().sign().inject()

        # Assert
        ...

    def test_3_create_transaction(self) -> None:
        # Arrange
        # FIXME: bootstrap1 private key. Move constants from tezos-init-sandboxed-client.sh script to parameters
        client = self.get_client().using(key='edsk3gUfUPyBSfrS9CCgmCiQsTCHGkviBDusMxDJstFtojtc1zcpsh')

        # Act
        op = client.transaction(
            source=sandbox_addresses['bootstrap1'],
            destination=sandbox_addresses['bootstrap2'],
            amount=42,
        )

        # FIXME: fill() magic!
        op.branch = client.shell.blocks()[0][0]
        op.protocol = sandbox_protocols['PtEdo2Zk']

        op.fill().sign().inject()

        # Assert
        ...

    def test_4_bake_block(self) -> None:
        # Arrange
        client = self.get_client()
        client.loglevel = 'DEBUG'

        # Act
        op = client.bake_block()
        # FIXME: proto.008-PtEdo2Zk.operation.not_enough_endorsements_for_priority
        op.fill().sign().inject()

        # Assert
        ...
