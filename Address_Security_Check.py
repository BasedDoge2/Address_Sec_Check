import requests
from datetime import datetime
import math


Etherscan_API_Keys = input("Copy and Paste your Etherscan_API_Key:")
cumulative_timescore = 0
transaction_count_score = 0
balance = 0
general_sec_score = 0

print("Hello, welcome to Address Security Check, an open source security tool used to vet Ethereum addresses for suspicious actors")
print("-" * 40)
print("What address would you like to check")
Address = input("Submit address here: ")
print("You may check the balance, transaction count, tornado cash interactions, and age - first transactions of receiving and sending tokens, and funding source of an address")
Choice = input("What would you like to do (balance/transaction count/tornado cash interactions/age/all): ")

# list of tornado cash addresses from Office of Foreign Asset Control - https://ofac.treasury.gov/recent-actions/20220808
tornado_cash_address_string = "0x8589427373D6D84E98730D7795D8f6f8731FDA16, 0x722122dF12D4e14e13Ac3b6895a86e84145b6967, 0xDD4c48C0B24039969fC16D1cdF626eaB821d3384, 0xd90e2f925DA726b50C4Ed8D0Fb90Ad053324F31b, 0xd96f2B1c14Db8458374d9Aca76E26c3D18364307, 0x4736dCf1b7A3d580672CcE6E7c65cd5cc9cFBa9D, 0xD4B88Df4D29F5CedD6857912842cff3b20C8Cfa3, 0x910Cbd523D972eb0a6f4cAe4618aD62622b39DbF, 0xA160cdAB225685dA1d56aa342Ad8841c3b53f291, 0xFD8610d20aA15b7B2E3Be39B396a1bC3516c7144, 0xF60dD140cFf0706bAE9Cd734Ac3ae76AD9eBC32A, 0x22aaA7720ddd5388A3c0A3333430953C68f1849b, 0xBA214C1c1928a32Bffe790263E38B4Af9bFCD659, 0xb1C8094B234DcE6e03f10a5b673c1d8C69739A00, 0x527653eA119F3E6a1F5BD18fbF4714081D7B31ce, 0x58E8dCC13BE9780fC42E8723D8EaD4CF46943dF2, 0xD691F27f38B395864Ea86CfC7253969B409c362d, 0xaEaaC358560e11f52454D997AAFF2c5731B6f8a6, 0x1356c899D8C9467C7f71C195612F8A395aBf2f0a, 0xA60C772958a3eD56c1F15dD055bA37AC8e523a0D, 0x169AD27A470D064DEDE56a2D3ff727986b15D52B, 0x0836222F2B2B24A3F36f98668Ed8F0B38D1a872f, 0xF67721A2D8F736E75a49FdD7FAd2e31D8676542a, 0x9AD122c22B14202B4490eDAf288FDb3C7cb3ff5E, 0x905b63Fff465B9fFBF41DeA908CEb12478ec7601, 0x07687e702b410Fa43f4cB4Af7FA097918ffD2730, 0x94A1B5CdB22c43faab4AbEb5c74999895464Ddaf, 0xb541fc07bC7619fD4062A54d96268525cBC6FfEF, 0x12D66f87A04A9E220743712cE6d9bB1B5616B8Fc, 0x47CE0C6eD5B0Ce3d3A51fdb1C52DC66a7c3c2936, 0x23773E65ed146A459791799d01336DB287f25334, 0xD21be7248e0197Ee08E0c20D4a96DEBdaC3D20Af, 0x610B717796ad172B316836AC95a2ffad065CeaB4, 0x178169B423a011fff22B9e3F3abeA13414dDD0F1, 0xbB93e510BbCD0B7beb5A853875f9eC60275CF498, 0x2717c5e28cf931547B621a5dddb772Ab6A35B701, 0x03893a7c7463AE47D46bc7f091665f1893656003, 0xCa0840578f57fE71599D29375e16783424023357, 0x58E8dCC13BE9780fC42E8723D8EaD4CF46943dF2, 0x8589427373D6D84E98730D7795D8f6f8731FDA16, 0x722122dF12D4e14e13Ac3b6895a86e84145b6967, 0xDD4c48C0B24039969fC16D1cdF626ea"
tornado_cash_addresses_list = [address.strip().lower() for address in tornado_cash_address_string.split(',')]

# Function to get address info from etherscan
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

# Function using get_address_info to retrieve balance of a given wallet
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

# Function to get a given address and its transaction info from etherscan
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

# Function to print transaction data, converts timestamp to UTC
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

# Function that counts all observable transactions for a given address and calculates a score given transaction count
def transaction_count(address):
    global transaction_count_score
    transaction_count_score = 0
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

# Function to check for the age of transactions, finding the first received and sent transactions
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
        global cumulative_timescore
        cumulative_timescore = (first_received_transaction_timescore + first_sent_transaction_timescore) / 2
        print(f"The cumulative timescore is {cumulative_timescore}")
    else:
        print("\nNo transactions found for the given address.")

# Function to check for Tornado Cash interactions, uses the list above
def tornado_cash_check(address):
    address_info = get_address_transaction_info(address)
    global tornado_cash_interactions 
    tornado_cash_interactions= False
    if address_info.get("status") == "1":
        transactions = address_info.get("result")
        for transaction in transactions:
            from_address = transaction['from'].lower()
            to_address = transaction['to'].lower()
            
            if from_address in tornado_cash_addresses_list or to_address in tornado_cash_addresses_list:
                tornado_cash_interactions = True
    if tornado_cash_interactions:
        print("Warning, this Address has interacted with Tornado Cash, a US Sanctioned money laundering service")
    else:
        print("No interactions with Tornado Cash found")

if Choice.lower() == "balance" or Choice.lower() == "all":
    check_balance(Address)
if Choice.lower() == "tornado cash interactions" or Choice.lower() == "all":
    tornado_cash_check(Address)
if Choice.lower() == "transaction count" or Choice.lower() == "all":
    transaction_count(Address)
if Choice.lower() == "age" or Choice.lower() == "all":
    age(Address)
if Choice.lower() not in ["balance", "transaction count", "age", "all"]:
    print("\nInvalid choice. Please choose 'balance', 'transaction count', 'age', or 'all'.")
if Choice.lower() == "all":
    general_sec_score = (cumulative_timescore + transaction_count_score) / 2
    print(f"\nGeneral Security Score: {general_sec_score}")
