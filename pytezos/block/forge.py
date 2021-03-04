from datetime import datetime
from typing import Any
from typing import Dict

from pytezos.michelson.forge import forge_base58
from pytezos.michelson.forge import forge_int


def forge_block_header(content: Dict[str, Any]) -> bytes:
    print(content)
    res = forge_int(content['level'])
    res += forge_int(content['proto'])
    res += forge_base58(content['predecessor'])
    res += forge_int(int(datetime.strptime(content['timestamp'], '%Y-%m-%dT%H:%M:%SZ').timestamp()))
    res += forge_int(content['validation_pass'])
    res += forge_base58(content['operations_hash'])
    forged_fitness = content['fitness'][0].encode() + content['fitness'][1].encode()
    res += forge_int(len(forged_fitness))
    res += forged_fitness
    res += forge_base58(content['context'])
    return res
