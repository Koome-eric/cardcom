from flask import Flask, render_template_string
import requests
import datetime

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():

    def determine_tag(amount):
        tags_mapping = {
            300: "Learning sponsorship",
            350: "PWI Paid",
            500: "Kiddish Sponsored",
            2600: "Membership Paid",
            200: "Membership Paid",
            1000: "Membership Paid"
        }
        return tags_mapping.get(amount, "General donation")

    current_date = datetime.datetime.now().date()
    previous_day = current_date - datetime.timedelta(days=1)

    transactionsEndpoint = "https://secure.cardcom.solutions/api/v11/Transactions/ListTransactions"
    webhook_url = "https://hooks.zapier.com/hooks/catch/8868151/39x5zlt/"

    payload = {
        "ApiName": "1wq46yBe94ZntGBXdohR",
        "ApiPassword": "gnrBVd8oCM6eou3oeb1x",
        "TerminalNumber": "34375",
        "FromDate": previous_day.strftime('%d%m%Y'),
        "ToDate": previous_day.strftime('%d%m%Y'),
        "TranStatus": "Success",
        "Page": 1,
        "Page_size": 100,
        "LimitForTerminal": "your_terminal_number_here"
    }

    response = requests.post(transactionsEndpoint, json=payload)
    html_string = "<h1>Extracted Data</h1>"

    if response.status_code == 200:
        data = response.json()

        for transaction in data.get('Tranzactions', []):
            tag = determine_tag(transaction['Amount'])

            html_string += f"""
            <div>
                <p><strong>Transaction ID:</strong> {transaction['TranzactionId']}</p>
                <p><strong>Amount:</strong> {transaction['Amount']}</p>
                <p><strong>Card Owner Name:</strong> {transaction['CardOwnerName']}</p>
                <p><strong>Card Owner Email:</strong> {transaction['CardOwnerEmail']}</p>
                <p><strong>Card Owner Phone:</strong> {transaction['CardOwnerPhone']}</p>
                <p><strong>Tag:</strong> {tag}</p>
                <hr>
            </div>
            """
            
            transaction_data = {
                "Transaction ID": transaction['TranzactionId'],
                "Product Purchased": transaction['Description'],
                "Amount": transaction['Amount'],
                "Card Owner Name": transaction['CardOwnerName'],
                "Card Owner Email": transaction['CardOwnerEmail'],
                "Card Owner Phone": transaction['CardOwnerPhone'],
                "Transaction Date": transaction['CreateDate'],
                "Tag": tag
            }

            webhook_response = requests.post(webhook_url, json=transaction_data)
            if webhook_response.status_code != 200:
                html_string += f"""
                <div>
                    <p style="color: red;">Failed to send data to webhook for Transaction ID: {transaction['TranzactionId']}. Status Code: {webhook_response.status_code}, Response: {webhook_response.text}</p>
                </div>
                """

    return render_template_string(html_string)

@app.errorhandler(404)
def page_not_found(e):
    return jsonify({"error": "404", "message": "Page not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
