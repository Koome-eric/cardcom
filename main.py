import requests
import datetime

def determine_tag(amount):
    # Mapping of amounts and their corresponding tags
    tags_mapping = {
        300: "Learning sponsorship",
        350: "PWI Paid",  # This might conflict since there are two 350 values with different tags in the data you provided.
        500: "Kiddish Sponsored",
        2600: "Membership Paid",
        200: "Membership Paid",  # seat for members
        1000: "Membership Paid"  # seat for non members
    }

    return tags_mapping.get(amount, "General donation")  # Default to "General donation" if no exact match is found

# Get current date and calculate the previous day
current_date = datetime.datetime.now().date()
previous_day = current_date - datetime.timedelta(days=1)

# API endpoint
transactionsEndpoint = "https://secure.cardcom.solutions/api/v11/Transactions/ListTransactions"
webhook_url = "https://hooks.zapier.com/hooks/catch/8868151/39x5zlt/"

payload = {
    "ApiName": "1wq46yBe94ZntGBXdohR",
    "ApiPassword": "gnrBVd8oCM6eou3oeb1x",
    "TerminalNumber": "34375",
    "FromDate": previous_day.strftime('%d%m%Y'),  # Set to previous day
    "ToDate": previous_day.strftime('%d%m%Y'),    # Set to previous day
    "TranStatus": "Success",
    "Page": 1,
    "Page_size": 100,
    "LimitForTerminal": "your_terminal_number_here"
}

response = requests.post(transactionsEndpoint, json=payload)

# Ensure the request was successful
if response.status_code == 200:
    data = response.json()
    
    # Loop through the transactions
for transaction in data.get('Tranzactions', []):
    tag = determine_tag(transaction['Amount'])
    
    print(f"Transaction ID: {transaction['TranzactionId']}")
    print(f"Amount: {transaction['Amount']}")
    print(f"Card Owner Name: {transaction['CardOwnerName']}")
    print(f"Card Owner Email: {transaction['CardOwnerEmail']}")
    print(f"Card Owner Phone: {transaction['CardOwnerPhone']}")
    print(f"Tag: {tag}")  # Print the determined tag
    print("--------------")  # Separator for better readability
    
    transaction_data = {
        "Transaction ID": transaction['TranzactionId'],
        "Product Purchased": transaction['Description'],
        "Amount": transaction['Amount'],
        "Card Owner Name": transaction['CardOwnerName'],
        "Card Owner Email": transaction['CardOwnerEmail'],
        "Card Owner Phone": transaction['CardOwnerPhone'],
        "Transaction Date": transaction['CreateDate'],
        "Tag": tag  # Adding the determined tag
    }

    # Send the transaction data to the webhook
    webhook_response = requests.post(webhook_url, json=transaction_data)

    # Optional: check the webhook response
    if webhook_response.status_code != 200:
        print(f"Failed to send data to webhook for Transaction ID: {transaction['TranzactionId']}. Status Code: {webhook_response.status_code}, Response: {webhook_response.text}")

