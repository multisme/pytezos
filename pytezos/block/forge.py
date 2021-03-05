import unittest
from datetime import datetime
from typing import Any
from typing import Dict

from pytezos.michelson.forge import forge_base58
from pytezos.michelson.forge import forge_int
from pytezos.michelson.forge import optimize_timestamp

DEFAULT_FITNESS = b'\x00\x00\x00\x11\x00\x00\x00\x01\x00\x00\x00\x00\x08\x00\x00\x00\x00\x00\x00\x00\x01'
DEFAULT_PROTOCOL_DATA = b'\x00\x00\xfb\x01\xfb\x62\x84\x9e\x12\xe6\x00\xab\x7a\xd9\x51\x7d\x54\xf7\x7a\x32\x3e\x49\x9c\x32\x10\x29\x17\x3c\xe7\xf0\x31\x76\x80\xf6\x60\x51\xb8\x99\x2e\xc6\x45\x80\x55\x57\xdb\xeb\x4e\x2b\xb6\xee\x43\x00\x9d\x0e\xdc\x4c\x4d\xaf\x06\xd1\x24\x33\x65\x03\x8a\xa9\x9c\x8f\x07\xce\x3a\xb1\x3a\xe8\x06'


def forge_block_header(content: Dict[str, Any]) -> bytes:
    res = b'\x00\x00\x00'
    res += forge_int(content['level'])
    res += forge_int(content['proto'])
    res += forge_base58(content['predecessor'])

    res += b'\x00\x00\x00'
    # FIXME: Wrong timestamp. Timezone mismatch?
    res += forge_int(optimize_timestamp(content['timestamp']))

    res += forge_int(content['validation_pass'])
    res += forge_base58(content['operations_hash'])

    # FIXME: How to encode fitness?
    res += DEFAULT_FITNESS

    res += forge_base58(content['context'])

    # FIXME: What is protocol_data?
    res += DEFAULT_PROTOCOL_DATA
    return res
