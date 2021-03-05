from typing import Any
from typing import Dict
from typing import Optional

from pytezos.block.forge import DEFAULT_PROTOCOL_DATA
from pytezos.block.forge import forge_block_header
from pytezos.context.impl import ExecutionContext  # type: ignore
from pytezos.context.mixin import ContextMixin  # type: ignore
from pytezos.crypto.encoding import base58_encode
from pytezos.crypto.key import blake2b_32
from pytezos.michelson.forge import forge_base58
from pytezos.operation.content import ContentMixin

SANDBOX_DICTATOR_PRIVATE_KEY = "edsk31vznjHSSpGExDMHYASz45VZqXN4DPxvsa4hAyY8dHM28cZzp6"
DEFAULT_PROTOCOL = 'ProtoGenesisGenesisGenesisGenesisGenesisGenesk612im'
DEFAULT_PROTOCOL_PARAMETERS = {
    "bootstrap_accounts": [
        ["edpkuBknW28nW72KG6RoHtYW7p12T6GKc7nAbwYX5m8Wd9sDVC9yav", "4000000000000"],
        ["edpktzNbDAUjUk697W7gYg2CRuBQjyPxbEg8dLccYYwKSKvkPvjtV9", "4000000000000"],
        ["edpkuTXkJDGcFd5nh6VvMz8phXxU3Bi7h6hqgywNFi1vZTfQNnS1RV", "4000000000000"],
        ["edpkuFrRoDSEbJYgxRtLx2ps82UdaYc1WwfS9sE11yhauZt5DgCHbU", "4000000000000"],
        ["edpkv8EUUH68jmo3f7Um5PezmfGrRF24gnfLpH3sVNwJnV5bVCxL2n", "4000000000000"],
    ],
    "bootstrap_contracts": [],
    "commitments": [],
    "preserved_cycles": 2,
    "blocks_per_cycle": 8,
    "blocks_per_commitment": 4,
    "blocks_per_roll_snapshot": 4,
    "blocks_per_voting_period": 64,
    "time_between_blocks": ["1", "0"],
    "endorsers_per_block": 32,
    "hard_gas_limit_per_operation": "1040000",
    "hard_gas_limit_per_block": "10400000",
    "proof_of_work_threshold": "70368744177663",
    "tokens_per_roll": "8000000000",
    "michelson_maximum_type_size": 1000,
    "seed_nonce_revelation_tip": "125000",
    "origination_size": 257,
    "block_security_deposit": "512000000",
    "endorsement_security_deposit": "64000000",
    "baking_reward_per_endorsement": ["1250000", "187500"],
    "endorsement_reward": ["1250000", "833333"],
    "cost_per_byte": "250",
    "hard_storage_limit_per_operation": "60000",
    "test_chain_duration": "1966080",
    "quorum_min": 2000,
    "quorum_max": 7000,
    "min_proposal_quorum": 500,
    "initial_endorsers": 1,
    "delay_per_missing_endorsement": "1",
}
DEFAULT_PREAPPLY_BLOCK = {
    "protocol_data": {
        "protocol": "ProtoGenesisGenesisGenesisGenesisGenesisGenesk612im",
        "content": {
            "command": "activate",
            "hash": "PtEdo2ZkT9oKpimTah6x2embF25oss54njMuPzkJTEi5RqfdZFA",
            "fitness": ["00", "0000000000000001"],
            "protocol_parameters": "000005a4a405000004626f6f7473747261705f6163636f756e747300cc01000004300058000000023000370000006564706b75426b6e5732386e5737324b4736526f48745957377031325436474b63376e4162775958356d385764397344564339796176000231000e00000034303030303030303030303030000004310058000000023000370000006564706b747a4e624441556a556b36393757376759673243527542516a79507862456738644c63635959774b534b766b50766a745639000231000e00000034303030303030303030303030000004320058000000023000370000006564706b7554586b4a4447634664356e683656764d7a38706858785533426937683668716779774e466931765a5466514e6e53315256000231000e00000034303030303030303030303030000004330058000000023000370000006564706b754672526f445345624a59677852744c783270733832556461596331577766533973453131796861755a7435446743486255000231000e00000034303030303030303030303030000004340058000000023000370000006564706b76384555554836386a6d6f336637556d3550657a6d66477252463234676e664c70483373564e774a6e5635625643784c326e000231000e0000003430303030303030303030303000000004626f6f7473747261705f636f6e74726163747300050000000004636f6d6d69746d656e7473000500000000017072657365727665645f6379636c657300000000000000004001626c6f636b735f7065725f6379636c6500000000000000204001626c6f636b735f7065725f636f6d6d69746d656e7400000000000000104001626c6f636b735f7065725f726f6c6c5f736e617073686f7400000000000000104001626c6f636b735f7065725f766f74696e675f706572696f640000000000000050400474696d655f6265747765656e5f626c6f636b7300170000000230000200000031000231000200000030000001656e646f72736572735f7065725f626c6f636b00000000000000404002686172645f6761735f6c696d69745f7065725f6f7065726174696f6e0008000000313034303030300002686172645f6761735f6c696d69745f7065725f626c6f636b00090000003130343030303030000270726f6f665f6f665f776f726b5f7468726573686f6c64000f00000037303336383734343137373636330002746f6b656e735f7065725f726f6c6c000b0000003830303030303030303000016d696368656c736f6e5f6d6178696d756d5f747970655f73697a65000000000000408f4002736565645f6e6f6e63655f726576656c6174696f6e5f746970000700000031323530303000016f726967696e6174696f6e5f73697a6500000000000010704002626c6f636b5f73656375726974795f6465706f736974000a0000003531323030303030300002656e646f7273656d656e745f73656375726974795f6465706f73697400090000003634303030303030000462616b696e675f7265776172645f7065725f656e646f7273656d656e74002200000002300008000000313235303030300002310007000000313837353030000004656e646f7273656d656e745f726577617264002200000002300008000000313235303030300002310007000000383333333333000002636f73745f7065725f6279746500040000003235300002686172645f73746f726167655f6c696d69745f7065725f6f7065726174696f6e000600000036303030300002746573745f636861696e5f6475726174696f6e000800000031393636303830000171756f72756d5f6d696e000000000000409f400171756f72756d5f6d617800000000000058bb40016d696e5f70726f706f73616c5f71756f72756d000000000000407f4001696e697469616c5f656e646f727365727300000000000000f03f0264656c61795f7065725f6d697373696e675f656e646f7273656d656e740002000000310000",
        },
        "signature": "edsigtXomBKi5CTRf5cjATJWSyaRvhfYNHqSUGrn4SdbYRcGwQrUGjzEfQDTuqHhuA8b2d8NarZjz8TRf65WkpQmo423BtomS8Q",
    },
    "operations": [],
}


class BlockHeader(ContextMixin, ContentMixin):
    def __init__(
        self,
        context: ExecutionContext,
        content: Dict[str, Any],
        protocol: Optional[str] = None,
        signature: Optional[str] = None,
    ):
        super().__init__(context=context)
        self.content = content
        self.protocol = protocol
        self.signature = signature

    def _spawn(self, **kwargs):
        return BlockHeader(
            context=self.context,
            content=kwargs.get('content', self.content.copy()),
            protocol=kwargs.get('protocol', self.protocol),
            signature=kwargs.get('signature', self.signature),
        )

    def json_payload(self) -> dict:
        """Get json payload used for the preapply."""
        return DEFAULT_PREAPPLY_BLOCK

    def binary_payload(self) -> bytes:
        """Get binary payload used for injection/hash calculation."""
        if not self.signature:
            raise ValueError('Not signed')

        return bytes.fromhex(self.forge()) + forge_base58(self.signature)

    def forge(self, validate=True):
        """Convert json representation of the operation group into bytes.

        :param validate: Forge remotely also and compare results, default is True
        :returns: Hex string
        """

        response = self.shell.head.helpers.preapply.block.post(block=self.json_payload())
        response = response['shell_header']
        response['protocol_data'] = DEFAULT_PROTOCOL_DATA.hex()
        local_data = forge_block_header(response).hex()

        if validate:
            remote_data = self.shell.head.helpers.forge_block_header.post(block_header=response)['block']
            # if local_data != remote_data:
            #     raise ValueError(f'Local forge result differs from remote one:\n\n{local_data}\n\n{remote_data}')

        return local_data

    def sign(self):
        """Sign the operation group with the key specified by `using`.

        :rtype: BlockHeader
        """
        watermark = b'\x01'
        message = watermark + bytes.fromhex(self.forge())
        signature = self.key.sign(message=message, generic=True)

        return self._spawn(signature=signature)

    def hash(self) -> str:
        """Calculate the Base58 encoded operation group hash."""
        hash_digest = blake2b_32(self.binary_payload()).digest()
        return base58_encode(hash_digest, b'o').decode()

    def preapply(self):
        """Preapply signed block header.

        :returns: RPC response from `preapply`
        """
        if not self.signature:
            raise ValueError('Not signed')

        return self.shell.head.helpers.preapply.block.post(block=self.json_payload())['shell_header']

    def inject(self, _async=True, check_result=True, num_blocks_wait=5, time_between_blocks: Optional[int] = None):
        """Inject the signed block header.

        :param _async: do not wait for operation inclusion (default is True)
        :param preapply: do a preapply before injection
        :param check_result: raise RpcError in case operation is applied but has runtime errors
        :param num_blocks_wait: number of blocks to wait for injection
        :param time_between_blocks: override the corresponding parameter from constants
        :returns: operation group with metadata (raw RPC response)
        """
        self.context.reset()

        payload = self.binary_payload()
        opg_hash = self.shell.injection.block.post(block=payload, _async=False)

        if _async:
            return {'hash': opg_hash, **self.json_payload()}
