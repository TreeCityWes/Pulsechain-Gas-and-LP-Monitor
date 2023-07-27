Pulsechain LP Pair Monitoring Script

This Python script is designed to monitor the creation of current gas (beat) and new liquidity pool (LP) pairs on the Pulsechain network and record relevant information about those pairs in a text file. It utilizes the Web3.py library to interact with the Pulsechain blockchain.

Requirements
Python 3.x
Web3.py library (web3)

How it Works

The script connects to the Pulsechain blockchain through a free third-party API provided by Third Web.
  It initializes a contract object to interact with the Pulsechain Factory contract at the address pulsechain_factory using its ABI (pulsechain_factory_abi).
The handle_event function is defined to process events triggered by the contract. Specifically, it handles the "PairCreated" event, extracting relevant data such as the addresses of the two tokens involved in the pair, the pair address, and the block number when the event occurred.
  Inside the handle_event function, it tries to retrieve the token symbols of the two tokens using their contract addresses. If successful, it will display the symbols along with the other information about the newly created pair. If there is any error retrieving the token symbols, the script will log an error message but continue processing other events.
The script sets up a loop that continuously checks for new "PairCreated" events on the Pulsechain network.
  In the main function, an event filter is created to listen for new "PairCreated" events starting from the latest block.
The script enters an infinite loop to continuously check for new events. When a new event is detected, the handle_event function is called to process it.
  The script records the pair information in a text file named "new_pairs_pls.txt". For each new pair, it appends the pair address, token addresses, token symbols, and the block number to the file.
The loop sleeps for 11 seconds after processing each batch of events, allowing time for new events to be generated.

How to Run


Make sure you have Python 3.x installed on your system.

Install the required library web3. You can do this using pip:


bash
Copy code
pip install web3
Copy the provided script into a Python file (e.g., pulsechain_lp_monitor.py).

Run the script using Python:


bash
Copy code
python pulsechain_lp_monitor.py
The script will start monitoring the Pulsechain network for new LP pair creations and log the relevant information in the "new_pairs_pls.txt" file.


Note: This script assumes that you have a valid free Third Web Infura API URL and that the provided contract addresses (pulsechain_factory, pulsechain_router) are correct and correspond to the actual contracts on the Pulsechain network. Also, please ensure that you have appropriate permission to interact with the network and access the required contract events.
