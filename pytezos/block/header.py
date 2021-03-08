from pprint import pformat
from typing import Any
from typing import Dict
from typing import List
from typing import Optional

import bson  # type: ignore

from pytezos.block.forge import forge_protocol_data
from pytezos.context.impl import ExecutionContext  # type: ignore
from pytezos.context.mixin import ContextMixin  # type: ignore
from pytezos.crypto.encoding import base58_encode
from pytezos.crypto.key import blake2b_32
from pytezos.jupyter import get_class_docstring
from pytezos.michelson.forge import forge_array
from pytezos.michelson.forge import forge_base58


class BlockHeader(ContextMixin):
    def __init__(
        self,
        context: ExecutionContext,
        protocol_data: Optional[Dict[str, Any]] = None,
        operations: Optional[List[Dict[str, Any]]] = None,
        protocol: Optional[str] = None,
        signature: Optional[str] = None,
        data: Optional[bytes] = None,
    ):
        super().__init__(context=context)
        self.protocol_data = protocol_data or {}
        self.operations = operations or []
        self.protocol = protocol
        self.signature = signature
        self.data = data

    def __repr__(self):
        res = [
            super().__repr__(),
            '\nPayload',
            pformat(self.json_payload()),
            '\nHelpers',
            get_class_docstring(self.__class__),
        ]
        return '\n'.join(res)

    @classmethod
    def activate_protocol(cls, protocol_hash: str, parameters: Dict[str, Any], context: ExecutionContext) -> 'BlockHeader':
        protocol_data = {
            "content": {
                "command": "activate",
                "hash": protocol_hash,
                "fitness": ["00", "0000000000000001"],
                "protocol_parameters": forge_array(bson.dumps(parameters)).hex(),
            }
        }
        return BlockHeader(
            context=context,
            protocol_data=protocol_data,
        )

    @classmethod
    def bake_block(cls, context: ExecutionContext, min_fee: int = 0) -> 'BlockHeader':
        # 1. Query pending operations from the mempool (status == applied)
        # 2. Apply filters (e.g. select only operations with fee > min_fee) <-- optional
        # 3. Preapply block with selected operations
        # 4. There are 5 predefined baking accounts (bootstrap) specified in protocol parameters
        # 5. Check baking rights for the next level http://127.0.0.1:8732/chains/main/blocks/head/helpers/baking_rights to determine priority
        # 6. Use previous pow stamp (8 bytes) or zero for level 2
        # 7. Forge block header
        # 8. Sign block header
        # 9. Inject header and operations (forged)
        # See https://gitlab.com/nomadic-labs/tezos/-/blob/francois@test-forging-block/tests_python/tools/forge.py for the reference
        priority = 0
        baking_rights = context.shell.blocks.head.helpers.baking_rights()
        for item in baking_rights:
            if item['delegate'] == context.key.public_key_hash():
                priority = item['priority']

        protocol_data = {
            # FIXME: Hardcode
            "priority": priority,
            "proof_of_work_nonce": "DEADBEEFDEADBEEF",
        }

        max_operations = context.shell.block()['metadata']['max_operation_list_length'][0]['max_op']
        operations: List[Dict[str, Any]] = []

        for status, pending_opg in context.shell.mempool.pending_operations().items():
            if status != 'applied':
                continue
            for pending_op in pending_opg:
                if int(pending_op['contents'][0]['fee']) >= min_fee:
                    operations.append(pending_op)
                if len(operations) == max_operations:
                    break

        return BlockHeader(
            context=context,
            operations=operations,
            protocol_data=protocol_data,
        )


    def _spawn(self, **kwargs):
        return BlockHeader(
            context=self.context,
            protocol_data=kwargs.get('protocol_data', self.protocol_data.copy()),
            protocol=kwargs.get('protocol', self.protocol),
            signature=kwargs.get('signature', self.signature),
            data=kwargs.get('data', self.data),
        )

    def fill(self) -> 'BlockHeader':
        """Fill the protocol field

        :rtype: BlockHeader
        """
        res = self.shell.head.protocols()
        return self._spawn(protocol=res['next_protocol'])

    def json_payload(self) -> dict:
        """Get json payload used for the preapply."""
        signature = self.signature
        if signature is None:
            signature = base58_encode(b'\x00' * 64, b'sig').decode()  # null signature, works for preapply

        return {
            "protocol_data": {
                "protocol": self.protocol,
                **self.protocol_data,
                "signature": signature,
            },
            "operations": self.operations,
        }

    def binary_payload(self) -> bytes:
        """Get binary payload used for injection/hash calculation."""
        if self.signature is None:
            raise ValueError('Not signed')
        if self.data is None:
            raise ValueError('No data')
        return self.data + forge_base58(self.signature)

    def forge(self) -> 'str':
        """Convert json representation of the operation group into bytes.

        :returns: Hex string
        """
        header = self.preapply()
        header['protocol_data'] = forge_protocol_data(self.protocol_data).hex()
        res = self.shell.head.helpers.forge_block_header.post(block_header=header)
        return res['block']

    def sign(self):
        """Sign the operation group with the key specified by `using`.

        :rtype: BlockHeader
        """
        chain_watermark = bytes.fromhex(self.shell.chains.main.watermark())
        watermark = b'\x01' + chain_watermark
        data = bytes.fromhex(self.forge())
        signature = self.key.sign(message=watermark + data)
        return self._spawn(signature=signature, data=data)

    def hash(self) -> str:
        """Calculate the Base58 encoded operation group hash."""
        hash_digest = blake2b_32(self.binary_payload()).digest()
        return base58_encode(hash_digest, b'B').decode()

    def preapply(self):
        """Preapply block

        :returns: shell header and operations
        """
        if self.protocol is None:
            raise ValueError('current protocol is not specified')

        res = self.shell.head.helpers.preapply.block.post(block=self.json_payload())
        # TODO: handle errored operations https://tezos.gitlab.io/alpha/rpc.html#post-block-id-helpers-preapply-block
        return res['shell_header']

    def inject(self, _async=False, force=False):
        """Inject the signed block header.

        :returns: block hash
        """
        block = {
            "data": self.binary_payload().hex(),
            "operations": self.operations,
        }
        return self.shell.injection.block.post(block=block, _async=_async, force=force)
