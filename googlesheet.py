# GoogleSheet_Campaign2.py
import os
import json
import datetime
import gspread
from google.oauth2.service_account import Credentials
import logging

logging.basicConfig(level=logging.INFO)

# -----------------------------
# Google Sheets Setup
# -----------------------------
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

CREDS = None
CLIENT = None
SPREADSHEET = None
SHEET = None
CLIENT_EMAIL = None

try:
    with open("ServiceAccount.json", "r", encoding="utf-8") as f:
        svc = json.load(f)
        CLIENT_EMAIL = svc.get("client_email")

    CREDS = Credentials.from_service_account_file(
        "ServiceAccount.json",
        scopes=SCOPE
    )
    CLIENT = gspread.authorize(CREDS)
    SPREADSHEET = CLIENT.open("ChatBotData")
    SHEET = SPREADSHEET.worksheet("Campaign2")

    logging.info(f"Connected as {CLIENT_EMAIL}")

except Exception:
    logging.exception("Failed to initialize Google Sheets client.")
    SHEET = None

# -----------------------------
# Sheet Headers
# -----------------------------
HEADERS = [
    "Name",
    "DOB",
    "User_Age",
    "Child_Age",
    "Monthly_Saving",
    "Education_Savings",
    "Phone",
    "Email",
    "Timestamp",
    "WhatsApp_Link"
]

# -----------------------------
# Ensure header exists (ROW 1 ONLY)
# -----------------------------
def ensure_header():
    if SHEET is None:
        return

    try:
        first_row = SHEET.row_values(1)

        if not first_row:
            SHEET.update("A1:J1", [HEADERS])
            logging.info("Header written to row 1")

    except Exception:
        logging.exception("Failed to ensure header")

# -----------------------------
# Save chatbot session (NO OVERWRITE)
# -----------------------------
def save_to_sheet(session):
    """
    Inserts data strictly into the next empty row.
    NEVER overwrites existing data.
    """
    if SHEET is None:
        logging.warning("Sheet unavailable. Skipping save.")
        return None

    ensure_header()

    phone = session.get("phone", "")
    whatsapp_link = f"https://wa.me/{phone}" if phone else ""

    row = [
        session.get("name", ""),
        session.get("dob", ""),
        session.get("user_age", ""),
        session.get("child_age", ""),
        session.get("budget", ""),
        session.get("education_savings", ""),
        phone,
        session.get("email", ""),
        datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        whatsapp_link
    ]

    try:
        # 🔒 RELIABLE NEXT EMPTY ROW LOGIC
        existing_rows = SHEET.get_all_values()
        next_row_index = len(existing_rows) + 1

        SHEET.insert_row(row, next_row_index)
        logging.info(f"Data inserted at row {next_row_index}")

        return next_row_index

    except Exception:
        logging.exception("Failed to insert row")
        return None

# -----------------------------
# Test connection helper
# -----------------------------
def test_sheet_connection(do_write=False):
    if SHEET is None:
        return {"ok": False, "error": "Sheet not initialized"}

    try:
        info = {
            "ok": True,
            "spreadsheet": SPREADSHEET.title,
            "worksheet": SHEET.title,
            "row_count": len(SHEET.get_all_values()),
            "client_email": CLIENT_EMAIL
        }

        if do_write:
            test_row = ["__TEST__", datetime.datetime.now().isoformat()]
            idx = len(SHEET.get_all_values()) + 1
            SHEET.insert_row(test_row, idx)
            info["write_ok"] = True

        return info

    except Exception as e:
        logging.exception("Test failed")
        return {"ok": False, "error": str(e)}
