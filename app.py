import os, json
from flask import Flask, jsonify
import gspread
from google.oauth2.service_account import Credentials

app = Flask(__name__)

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SPREADSHEET_ID = "1lT5v9iA4x1n8xdzDTQiUWqIh4GBfqnvnNe-8gyNQT5Q"
SHEET_NAME = "Clients"  # لازم يكون مطابق 100%

def get_sheet():
    sa_json = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON")
    info = json.loads(sa_json)

    creds = Credentials.from_service_account_info(info, scopes=SCOPES)
    client = gspread.authorize(creds)

    return client.open_by_key(SPREADSHEET_ID).worksheet(SHEET_NAME)

@app.route("/")
def home():
    return {"status": "249Group API is running"}

@app.route("/clients")
def get_clients():
    sheet = get_sheet()
    records = sheet.get_all_records()
    return jsonify(records)

@app.route("/client/<client_id>")
def get_client(client_id):
    sheet = get_sheet()
    records = sheet.get_all_records()

    for row in records:
        if str(row.get("client_id")) == client_id:
            return jsonify(row)

    return jsonify({"error": "Client not found"}), 404
