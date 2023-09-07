# Address Security Check

Welcome to Address Security Check, an open-source security tool used to vet Ethereum addresses for suspicious activities. This tool allows you to check various aspects of an Ethereum address, including its balance, transaction count, Tornado Cash interactions, and transaction age. You can use it to assess the security of an address before engaging with it.

## Getting Started

### Prerequisites

Before you begin, make sure you have the following prerequisites:

- Python 3.x installed on your machine.
- An Etherscan API key. You can obtain one by signing up at [Etherscan API](https://etherscan.io/apis).

### Installation

1. Clone this GitHub repository to your local machine: git clone https://github.com/your_username/Address-Security-Check.git

2. Navigate to the project directory: cd Address-Security-Check


3. Open the `address_security_check.py` file and replace `'YOUR_ETHERSCAN_API_KEY'` with your Etherscan API key:

Etherscan_API_Keys = input("Copy and Paste your Etherscan_API_Key:")

### Usage

Run the script by executing the following command in your terminal: python address_security_check.py

Follow the on-screen prompts to use the tool:

1. Enter the Ethereum address you want to check.
2. Choose from the following options:
- Balance: Check the balance of the address.
- Transaction count: Check the transaction count of the address.
- Tornado cash interactions: Check if the address has interacted with Tornado Cash.
- Age: Check the age of the address's first received and sent transactions.
- All: Perform all checks.

### Results

The tool will provide you with the following information:

- Balance of the address (if selected).
- Tornado Cash interactions (if selected).
- Transaction count and security score (if selected), the max security score for transaction count is 10 with 1000 transactions.
- Age of the first received and sent transactions (if selected), the security score for age is based on the age of the first transaction, with earlier transactions indicating a long term wallet.
- General security score (if all is selected), calculated based on transaction count score and age score.

### Contributing

If you would like to contribute to this project, follow the guidelines below:

1. Fork the repository on GitHub.
2. Create a new branch for your feature or bug fix.
3. Make your changes and test them thoroughly.
4. Commit your changes with clear and concise commit messages.
5. Push your branch to your fork on GitHub.
6. Open a pull request to the main branch of this repository.

### Acknowledgments
Thanks to Etherscan for providing the API that makes this tool possible.
This project uses data from the Office of Foreign Asset Control to identify Tornado Cash addresses.

Feel free to use, modify, and distribute this tool as needed. If you encounter any issues or have suggestions for improvements, please open an issue on GitHub. Happy secure Ethereum address checking!


