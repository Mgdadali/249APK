import os, json
from flask import Flask, jsonify
import gspread
from google.oauth2.service_account import Credentials

app = Flask(__name__)

SPREADSHEET_NAME = "249Group – Clients Tracking"
SHEET_NAME = "Clients"

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

def get_sheet():
    sa_json = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON")
    if not sa_json:
        raise RuntimeError("Missing GOOGLE_SERVICE_ACCOUNT_JSON env var")

    info = json.loads(sa_json)
    creds = Credentials.from_service_account_info(info, scopes=SCOPES)
    client = gspread.authorize(creds)
    return client.open(SPREADSHEET_NAME).worksheet(SHEET_NAME)

def row_to_dict(row, headers):
    return dict(zip(headers, row))

@app.route("/clients", methods=["GET"])
def get_clients():
    sheet = get_sheet()
    data = sheet.get_all_values()
    headers = data[0]
    rows = data[1:]
    return jsonify([row_to_dict(r, headers) for r in rows])

@app.route("/client/<client_id>", methods=["GET"])
def get_client(client_id):
    sheet = get_sheet()
    data = sheet.get_all_values()
    headers = data[0]
    for r in data[1:]:
        if r[0] == client_id:
            return jsonify(row_to_dict(r, headers))
    return jsonify({"error": "Client not found"}), 404
