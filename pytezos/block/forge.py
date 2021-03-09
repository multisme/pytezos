from typing import Any
from typing import Dict
from typing import List

from pytezos.michelson.forge import forge_array
from pytezos.michelson.forge import forge_base58


def forge_command(command):
    if command == 'activate':
        return b'\x00'
    else:
        raise NotImplementedError(command)


def forge_fitness(fitness: List[str]) -> bytes:
    return forge_array(b''.join(map(lambda x: forge_array(bytes.fromhex(x)), fitness)))


def forge_priority(priority: int) -> bytes:
    return priority.to_bytes(2, 'big')


def forge_content(content: Dict[str, Any]) -> bytes:
    res = b''
    res += forge_command(content.get('command'))
    res += forge_base58(content['hash'])
    res += forge_fitness(content['fitness'])
    res += bytes.fromhex(content['protocol_parameters'])
    return res


def forge_protocol_data(protocol_data: Dict[str, Any]):
    res = b''
    if protocol_data.get('content'):
        res += forge_content(protocol_data['content'])
    else:
        res += forge_priority(protocol_data['priority'])
        res += bytes.fromhex(protocol_data['proof_of_work_nonce'])
        if protocol_data.get('seed_nonce_hash'):
            res += b'\x01'
            res += bytes.fromhex(protocol_data['seed_nonce_hash'])
        else:
            res += b'\x00'
    return res
