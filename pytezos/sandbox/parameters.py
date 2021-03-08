sandbox_protocols = {
    'PtEdo2Zk': 'PtEdo2ZkT9oKpimTah6x2embF25oss54njMuPzkJTEi5RqfdZFA'
}

sandbox_addresses = {
    'activator': 'tz1TGu6TN5GSez2ndXXeDX6LgUDvLzPLqgYV',
    'bootstrap5': 'tz1ddb9NMYHZi5UzPdzTZMYQQZoMub195zgv',
    'bootstrap4': 'tz1b7tUupMgCNw2cCLpKTkSD1NZzB5TkP2sv',
    'bootstrap3': 'tz1faswCTDciRzE4oJ9jn2Vm2dvjeyA9fUzU',
    'bootstrap2': 'tz1gjaF81ZRRvdzjobyfVNsAeSC6PScjfQwN',
    'bootstrap1': 'tz1KqTpEZ7Yob7QbPE4Hy4Wo8fHG8LhKxZSx',
}

sandbox_params = {
    'bootstrap_accounts': [
        ['edpkuBknW28nW72KG6RoHtYW7p12T6GKc7nAbwYX5m8Wd9sDVC9yav', '4000000000000'],
        ['edpktzNbDAUjUk697W7gYg2CRuBQjyPxbEg8dLccYYwKSKvkPvjtV9', '4000000000000'],
        ['edpkuTXkJDGcFd5nh6VvMz8phXxU3Bi7h6hqgywNFi1vZTfQNnS1RV', '4000000000000'],
        ['edpkuFrRoDSEbJYgxRtLx2ps82UdaYc1WwfS9sE11yhauZt5DgCHbU', '4000000000000'],
        ['edpkv8EUUH68jmo3f7Um5PezmfGrRF24gnfLpH3sVNwJnV5bVCxL2n', '4000000000000']
    ],
    'bootstrap_contracts': [],
    'commitments': [],
    'preserved_cycles': 2.0,
    'blocks_per_cycle': 8.0,
    'blocks_per_commitment': 4.0,
    'blocks_per_roll_snapshot': 4.0,
    'blocks_per_voting_period': 64.0,
    'time_between_blocks': ['1', '0'],
    'endorsers_per_block': 32.0,
    'hard_gas_limit_per_operation': '1040000',
    'hard_gas_limit_per_block': '10400000',
    'proof_of_work_threshold': '70368744177663',
    'tokens_per_roll': '8000000000',
    'michelson_maximum_type_size': 1000.0,
    'seed_nonce_revelation_tip': '125000',
    'origination_size': 257.0,
    'block_security_deposit': '512000000',
    'endorsement_security_deposit': '64000000',
    'baking_reward_per_endorsement': ['1250000', '187500'],
    'endorsement_reward': ['1250000', '833333'],
    'cost_per_byte': '250',
    'hard_storage_limit_per_operation': '60000',
    'test_chain_duration': '1966080',
    'quorum_min': 2000.0,
    'quorum_max': 7000.0,
    'min_proposal_quorum': 500.0,
    'initial_endorsers': 1.0,
    'delay_per_missing_endorsement': '1'
}


def get_protocol_hash(alias):
    if alias not in sandbox_protocols:
        raise KeyError(f'Unsupported protocol alias: {alias}')
    return sandbox_protocols[alias]


def get_protocol_parameters(alias):
    return sandbox_params
