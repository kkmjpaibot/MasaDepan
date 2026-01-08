from flask import Flask, render_template, request, jsonify
import datetime
import re
import logging

# Google Sheets
from googlesheet import save_to_sheet

# Campaign 2 Email Service
from EmailService import send_campaign2_email

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# --------------------------
# Education Fund Calculation
# --------------------------
def calculate_education_fund(child_age, monthly_saving):
    years_to_uni = 18 - child_age
    annual_contribution = monthly_saving * 12

    def future_value(pmt, r, n):
        return pmt * (((1 + r) ** n - 1) / r)

    return {
        "child_age": child_age,
        "years_to_uni": years_to_uni,
        "annual_contribution": annual_contribution,
        "fv_6": future_value(annual_contribution, 0.06, years_to_uni),
        "fv_8": future_value(annual_contribution, 0.08, years_to_uni),
        "fv_10": future_value(annual_contribution, 0.10, years_to_uni)
    }

# --------------------------
# Routes
# --------------------------
@app.route("/")
def index():
    return render_template("Chatbot.html")

@app.route("/submit", methods=["POST"])
def submit():
    data = request.json

    # --------------------------
    # Parse input
    # --------------------------
    try:
        name = data.get("name", "").strip()
        dob = data.get("dob", "")
        child_age = int(data.get("child_age"))
        monthly = float(data.get("budget"))
        phone = data.get("phone", "")
        email = data.get("email", "")
        education_savings = data.get("education_savings", "None")
    except Exception:
        return jsonify({"error": "Invalid input data"}), 400

    # --------------------------
    # DOB validation
    # --------------------------
    if not re.match(r"^\d{2}/\d{2}/\d{4}$", dob):
        return jsonify({"error": "Invalid Date of Birth format (DD/MM/YYYY)"}), 400

    try:
        d, m, y = map(int, dob.split("/"))
        birth = datetime.date(y, m, d)
        today = datetime.date.today()
        age = today.year - birth.year - (
            (today.month, today.day) < (birth.month, birth.day)
        )
    except:
        return jsonify({"error": "Invalid Date of Birth"}), 400

    if age < 18:
        return jsonify({"error": "User must be at least 18 years old"}), 400

    # --------------------------
    # Child age validation
    # --------------------------
    if not 1 <= child_age <= 17:
        return jsonify({"error": "Child age must be between 1 and 17"}), 400

    # --------------------------
    # Monthly saving validation
    # --------------------------
    if monthly <= 0:
        return jsonify({"error": "Monthly saving must be positive"}), 400

    # --------------------------
    # Phone validation (Malaysia)
    # --------------------------
    if not re.match(r"^(\+60|60)[0-9]{9}$|^01[0-9]{8}$", phone):
        return jsonify({"error": "Invalid Malaysian phone number"}), 400

    # --------------------------
    # Email validation
    # --------------------------
    if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email):
        return jsonify({"error": "Invalid Email format"}), 400

    # --------------------------
    # Calculate education fund
    # --------------------------
    result = calculate_education_fund(child_age, monthly)
    result["user_age"] = age

    # --------------------------
    # Prepare data for Google Sheet + Email
    # --------------------------
    session_data = {
        "name": name,
        "dob": dob,
        "user_age": age,
        "child_age": child_age,
        "budget": monthly,
        "education_savings": education_savings,
        "phone": phone,
        "email": email
    }

    # --------------------------
    # Save to Google Sheets
    # --------------------------
    try:
        row_index = save_to_sheet(session_data)
        result["sheet_status"] = (
            f"Saved to Google Sheet row {row_index}"
            if row_index else
            "Failed to save to Google Sheet"
        )
    except Exception:
        logging.exception("Google Sheet save failed")
        result["sheet_status"] = "Failed to save to Google Sheet"

    # --------------------------
    # Send summary email (NON-BLOCKING)
    # --------------------------
    try:
        email_ok = send_campaign2_email(email, session_data, result)
        result["email_status"] = (
            "Summary email sent successfully"
            if email_ok else
            "Email sending failed"
        )
    except Exception:
        logging.exception("Email sending failed")
        result["email_status"] = "Email sending failed"

    # --------------------------
    # WhatsApp link
    # --------------------------
    result["whatsapp_link"] = f"https://wa.me/{phone}" if phone else ""

    return jsonify(result)

# --------------------------
# Run Flask
# --------------------------
if __name__ == "__main__":
    app.run(debug=True)
