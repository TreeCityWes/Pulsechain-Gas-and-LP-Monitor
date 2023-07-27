import json
from web3 import Web3
import asyncio

infura_url = 'https://pulsechain.rpc.thirdweb.com'
web3 = Web3(Web3.HTTPProvider(infura_url))

pulsechain_factory = '0x29eA7545DEf87022BAdc76323F373EA1e707C523'
pulsechain_router = '0x165C3410fC91EF562C50559f7d2289fEbed552d9'

pulsechain_factory_abi = [
    {
        "type": "constructor",
        "inputs": [
            {
                "type": "address",
                "name": "_feeToSetter",
                "internalType": "address"
            }
        ]
    },
    {
        "type": "function",
        "stateMutability": "view",
        "outputs": [
            {
                "type": "bytes32",
                "name": "",
                "internalType": "bytes32"
            }
        ],
        "name": "INIT_CODE_PAIR_HASH",
        "inputs": [],
        "constant": True
    },
    {
        "type": "function",
        "stateMutability": "view",
        "outputs": [
            {
                "type": "address",
                "name": "",
                "internalType": "address"
            }
        ],
        "name": "allPairs",
        "inputs": [
            {
                "type": "uint256",
                "name": "",
                "internalType": "uint256"
            }
        ],
        "constant": True
    },
    {
        "type": "function",
        "stateMutability": "view",
        "outputs": [
            {
                "type": "uint256",
                "name": "",
                "internalType": "uint256"
            }
        ],
        "name": "allPairsLength",
        "inputs": [],
        "constant": True
    },
    {
        "type": "function",
        "stateMutability": "nonpayable",
        "outputs": [
            {
                "type": "address",
                "name": "pair",
                "internalType": "address"
            }
        ],
        "name": "createPair",
        "inputs": [
            {
                "type": "address",
                "name": "tokenA",
                "internalType": "address"
            },
            {
                "type": "address",
                "name": "tokenB",
                "internalType": "address"
            }
        ],
        "constant": False
    },
    {
        "type": "function",
        "stateMutability": "view",
        "outputs": [
            {
                "type": "address",
                "name": "",
                "internalType": "address"
            }
        ],
        "name": "feeTo",
        "inputs": [],
        "constant": True
    },
    {
        "type": "function",
        "stateMutability": "view",
        "outputs": [
            {
                "type": "address",
                "name": "",
                "internalType": "address"
            }
        ],
        "name": "feeToSetter",
        "inputs": [],
        "constant": True
    },
    {
        "type": "function",
        "stateMutability": "view",
        "outputs": [
            {
                "type": "address",
                "name": "",
                "internalType": "address"
            }
        ],
        "name": "getPair",
        "inputs": [
            {
                "type": "address",
                "name": "",
                "internalType": "address"
            },
            {
                "type": "address",
                "name": "",
                "internalType": "address"
            }
        ],
        "constant": True
    },
    {
        "type": "function",
        "stateMutability": "nonpayable",
        "outputs": [],
        "name": "setFeeTo",
        "inputs": [
            {
                "type": "address",
                "name": "_feeTo",
                "internalType": "address"
            }
        ],
        "constant": False
    },
    {
        "type": "function",
        "stateMutability": "nonpayable",
        "outputs": [],
        "name": "setFeeToSetter",
        "inputs": [
            {
                "type": "address",
                "name": "_feeToSetter",
                "internalType": "address"
            }
        ],
        "constant": False
    },
    {
        "type": "event",
        "name": "PairCreated",
        "inputs": [
            {
                "type": "address",
                "name": "token0",
                "indexed": True
            },
            {
                "type": "address",
                "name": "token1",
                "indexed": True
            },
            {
                "type": "address",
                "name": "pair",
                "indexed": False
            },
            {
                "type": "uint256",
                "name": "",
                "indexed": False
            }
        ],
        "anonymous": False
    }
]

contract = web3.eth.contract(address=pulsechain_factory, abi=pulsechain_factory_abi)

def handle_event(event):
    pair_address = event['args']['pair']
    block_number = event['blockNumber']
    token0_address = event['args']['token0']
    token1_address = event['args']['token1']

    # Retrieve token symbols (if available)
    token0 = token0_address
    token1 = token1_address
    try:
        token0_contract = web3.eth.contract(address=token0_address, abi=uniswap_router_abi)
        token1_contract = web3.eth.contract(address=token1_address, abi=uniswap_router_abi)
        token0 = token0_contract.functions.symbol().call()
        token1 = token1_contract.functions.symbol().call()
    except Exception as e:
        print(f"Error retrieving token symbols: {e}")

    print("New LP pair created!")
    print("Token0 Address:", token0_address)
    print("Token0 Symbol:", token0)
    print("Token1 Address:", token1_address)
    print("Token1 Symbol:", token1)
    print("Pair Address:", pair_address)
    print("Block Number:", block_number)
    print("----------")

    # Append pair information to a text file
    with open("new_pairs_pls.txt", "a") as file:
        file.write(f"Pair: {pair_address}\n")
        file.write(f"Token0: {token0} ({token0_address})\n")
        file.write(f"Token1: {token1} ({token1_address})\n")
        file.write(f"Block Number: {block_number}\n")
        file.write("--------------------\n")

def main():
    event_filter = contract.events.PairCreated().create_filter(
        fromBlock='latest'
    )
    loop = asyncio.get_event_loop()
    while True:
        events = event_filter.get_new_entries()
        for event in events:
            handle_event(event)
        block_number = web3.eth.block_number
        gas_price = web3.eth.gas_price
        print(f"Waiting for new pair creations... (Block: {block_number}, Beat: {web3.from_wei(gas_price, 'gwei')} Beat)")
        loop.run_until_complete(asyncio.sleep(11))

if __name__ == '__main__':
    main()
