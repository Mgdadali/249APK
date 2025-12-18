from flask import Flask, jsonify
import gspread
from google.oauth2.service_account import Credentials

app = Flask(__name__)

# Google Sheet settings
SPREADSHEET_NAME = "249Group – Clients Tracking"
SHEET_NAME = "Clients"

# Auth
scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_file(
    "service_account.json",
    scopes=scopes
)

client = gspread.authorize(creds)
sheet = client.open(SPREADSHEET_NAME).worksheet(SHEET_NAME)


def row_to_dict(row, headers):
    return dict(zip(headers, row))


@app.route("/clients", methods=["GET"])
def get_clients():
    data = sheet.get_all_values()
    headers = data[0]
    rows = data[1:]

    clients = [row_to_dict(row, headers) for row in rows]
    return jsonify(clients)


@app.route("/client/<client_id>", methods=["GET"])
def get_client(client_id):
    data = sheet.get_all_values()
    headers = data[0]

    for row in data[1:]:
        if row[0] == client_id:
            return jsonify(row_to_dict(row, headers))

    return jsonify({"error": "Client not found"}), 404


if __name__ == "__main__":
    app.run(debug=True)
