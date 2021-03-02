from typing import TypedDict, Any


class OperationGroupContent(TypedDict, total=False):
    pkh: str
    source: str
    delegate: str
    counter: int
    secret: str
    period: int
    public_key: str
    fee: str
    gas_limit: str
    storage_limit: str
    kind: str
    metadata: Any