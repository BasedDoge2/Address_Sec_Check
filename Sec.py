import requests
from datetime import datetime
import math

Etherscan_API_Keys = "Y984B3E922EBXNGVKJQHF25B1B4PC53DQZ"
cumulative_timescore = 0
transaction_count_score = 0
balance = 0

print("Hello, welcome to Delance Account Check, an open source security tool used to vet Ethereum addresses for suspicious actors")
print("What address would you like to check")
Address = input("Submit address here: ")
print("You may check the balance of the address, transaction count security score, and age - first transactions of receiving and sending tokens, and funding source of an address")
Choice = input("What would you like to do (balance/transaction count/age/all): ")


def get_address_info(address):
    base_url = "https://api.etherscan.io/api"
    endpoint = "account"
    params = {
        "module": "account",
        "action": "balance",
        "address": address,
        "apikey": Etherscan_API_Keys  # Use the stored API key
    }
    
    response = requests.get(base_url, params=params)
    data = response.json()

    return data

def get_address_transaction_info(address):
    base_url = "https://api.etherscan.io/api"
    endpoint = "account"
    params = {
        "module": "account",
        "action": "txlist",
        "address": address,
        "startblock": "0",
        "endblock": "99999999",
        "page": "1", 
        "offset": "1000",
        "sort": "asc",
        "apikey": Etherscan_API_Keys  # Use the stored API key
    }
    
    response = requests.get(base_url, params=params)
    data = response.json()
    
    return data

def print_transaction_details(transaction):
    print("\nFirst Transaction Details:")
    print(f"Transaction Hash: {transaction['hash']}")
    print(f"Block Number: {transaction['blockNumber']}")
    timestamp = int(transaction['timeStamp'])
    utc_time = datetime.utcfromtimestamp(timestamp)
    current_year = datetime.utcnow().year
    year_difference = current_year - utc_time.year
    time_score = year_difference + 1  
    
    print(f"UTC Time: {utc_time}")
    print(f"Score: {time_score}")
    
    print(f"The first transaction of {Address} occurred at {utc_time} (UTC)")
    print(f"Value: {transaction['value']} wei")
    print(f"From: {transaction['from']}")
    print(f"To: {transaction['to']}") 
    print("-" * 40)  # Separator
    
    return time_score

def check_balance(address):
    address_info = get_address_info(address)
    if address_info.get("status") == "1":
        balance_wei = address_info.get("result")
        balance_eth = int(balance_wei) / 10**18
        print("-" * 40)
        print(f"\nBalance of {address}: {balance_eth} ETH")
        print("-" * 40)
    else:
        
        print("\nError retrieving address information")
        print("-" * 40)

def transaction_count(address):
    address_info = get_address_transaction_info(address)
    if address_info.get("status") == "1":
        transactions = address_info.get("result")
        transaction_count = len(transactions)
        max_score = 10  # Maximum score
        max_transaction_count = 1000  # Transaction count corresponding to max_score
        min_transaction_count = 1  # Minimum transaction count to avoid division by zero
        if transaction_count == 0:
            print("\nNo Recorded Transactions")
        elif transaction_count >= max_transaction_count:
            transaction_count_score = 10
        else:
            score = (transaction_count - 10) * (10 - 1) / (1000 - 10) + 1
            transaction_count_score = round(score, 2)
        print()
        print(f"There are {transaction_count} transactions.")
        print("-" * 40)
        print(f"Transaction count security score is: {transaction_count_score}")
        print("-" * 40)
        

def age(address):
    first_sent_transaction = None
    first_received_transaction = None
    address_info = get_address_transaction_info(address)
    if address_info.get("status") == "1":
        transactions = address_info.get("result")           
        for transaction in transactions:
            if transaction['from'].lower() == address.lower():
                if first_sent_transaction is None:
                    first_sent_transaction = transaction
                    timestamp = int(transaction['timeStamp'])
                    utc_time = datetime.utcfromtimestamp(timestamp)
                    current_year = datetime.utcnow().year
                    year_difference = current_year - utc_time.year
                    first_sent_transaction_timescore = year_difference + 1
            if transaction['to'].lower() == address.lower():
                if first_received_transaction is None:
                    first_received_transaction = transaction
                    timestamp = int(transaction['timeStamp'])
                    utc_time = datetime.utcfromtimestamp(timestamp)
                    current_year = datetime.utcnow().year
                    year_difference = current_year - utc_time.year
                    first_received_transaction_timescore = year_difference + 1
        
        if first_received_transaction is not None:
            print("\nFirst Received Transaction Details:")
            print_transaction_details(first_received_transaction)
            print(f"Received Transaction Time Score: {first_received_transaction_timescore}")
            print("-" * 40)
        else:
            print("\nNo First Received Transactions")
        
        if first_sent_transaction is not None:
            print("\nFirst Sent Transaction Details:")
            print_transaction_details(first_sent_transaction)
            print(f"Sent Transaction Time Score: {first_sent_transaction_timescore}")
            print("-" * 40)
        else:
            print("\nNo Sent Transactions")
        
        cumulative_timescore = (first_received_transaction_timescore + first_sent_transaction_timescore) / 2
        print(f"The cumulative timescore is {cumulative_timescore}")
    else:
        print("\nNo transactions found for the given address.")

if Choice.lower() == "balance" or Choice.lower() == "all":
    check_balance(Address)
if Choice.lower() == "transaction count" or Choice.lower() == "all":
    transaction_count(Address)
if Choice.lower() == "age" or Choice.lower() == "all":
    age(Address)
if Choice.lower() not in ["balance", "transaction count", "age", "all"]:
    print("\nInvalid choice. Please choose 'balance', 'transaction count', 'age', or 'all'.")
if Choice.lower() == "all":
    print("-" * 40)
    general_sec_score = (cumulative_timescore + transaction_count_score) / 2
    print(f"\nGeneral Security Score: {general_sec_score}")
