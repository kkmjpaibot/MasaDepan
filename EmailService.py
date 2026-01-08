# emailservice_campaign2.py
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import logging
import datetime
import os

# -----------------------------
# Configuration
# -----------------------------
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USERNAME = "kkmjpaibot@gmail.com"
SMTP_PASSWORD = "wkmi vjtc qtfg geph"  # Gmail App Password

FROM_EMAIL = SMTP_USERNAME
SUBJECT = "🎓 Your Child’s Education Planning Summary"
AGENT_WHATSAPP = "60168357258"  # No +

# -----------------------------
# Send Campaign 2 summary email
# -----------------------------
def send_campaign2_email(to_email, session_data, calc_result):
    """
    Sends a modern, visually appealing education savings summary email
    based on Campaign 2 chatbot data, with Benefits.pdf attached.
    """
    try:
        whatsapp_link = (
            f"https://wa.me/{AGENT_WHATSAPP}"
            "?text=Hi,%20I%20just%20received%20my%20education%20planning%20summary%20email%20and%20would%20like%20to%20know%20more."
        )

        body = f"""
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>Education Planning Summary</title>
  <style>
    /* Reset */
    body, html {{ margin:0; padding:0; font-family:'Segoe UI', Arial, sans-serif; }}
    a {{ text-decoration:none; }}
    
    /* General */
    body {{
      background: linear-gradient(135deg, #e0f7fa, #f0f4f8);
      padding: 24px 0;
    }}
    .container {{
      width: 100%;
      max-width: 620px;
      margin: 0 auto;
      background: #ffffff;
      border-radius: 16px;
      overflow: hidden;
      box-shadow: 0 12px 32px rgba(0,0,0,0.08);
    }}
    .header {{
      background: linear-gradient(135deg,#1a73e8,#4285f4,#34a853);
      padding: 32px;
      text-align: center;
      color: #ffffff;
    }}
    .header h1 {{ margin:0; font-size:24px; }}
    .header p {{ margin:6px 0 0; font-size:16px; color:#e0f2f1; }}
    
    .content {{ padding:32px; color:#333333; font-size:16px; line-height:1.6; }}
    
    .summary-table {{
      width: 100%;
      border-collapse: collapse;
      margin-top:20px;
      font-size:15px;
    }}
    .summary-table td {{
      padding:12px;
    }}
    .summary-table tr:nth-child(even) {{ background:#f9fafb; }}
    .summary-table td.label {{ color:#666; font-weight:500; width:50%; }}
    .summary-table td.value {{ font-weight:600; }}
    
    .projection {{
      margin-top:28px;
      padding:20px;
      background: linear-gradient(90deg, #e3f2fd, #f0f7ff);
      border-radius:12px;
      box-shadow: inset 0 0 8px rgba(0,0,0,0.03);
    }}
    .projection p.title {{ margin:0; font-size:16px; font-weight:600; }}
    .projection p.values {{ margin:8px 0 0; font-size:15px; line-height:1.6; }}
    
    .cta {{
      text-align:center;
      margin-top:32px;
    }}
    .cta a {{
      background:#25D366;
      color:#ffffff;
      padding:14px 32px;
      border-radius:32px;
      font-size:16px;
      font-weight:600;
      display:inline-block;
      transition: transform 0.2s ease;
    }}
    .cta a:hover {{ transform: scale(1.05); }}
    
    .footer {{
      margin-top:32px;
      font-size:14px;
      color:#666;
      text-align:center;
      line-height:1.5;
    }}
    .footer strong {{ color:#333; }}
  </style>
</head>

<body>
  <div class="container">
    <!-- Header -->
    <div class="header">
      <h1>Education Planning Assistant</h1>
      <p>Planning Today for Your Child’s Tomorrow</p>
    </div>

    <!-- Content -->
    <div class="content">
      <p>Hi <strong>{session_data.get('name','')}</strong> 👋,</p>
      <p>Thank you for taking the time to plan for your child’s education. Here’s a summary of what you shared during our chat:</p>

      <!-- Summary Table -->
      <table class="summary-table">
        <tr>
          <td class="label">🎂 Date of Birth</td>
          <td class="value">{session_data.get('dob','')} (Age: {session_data.get('user_age','')})</td>
        </tr>
        <tr>
          <td class="label">👶 Child Age</td>
          <td class="value">{session_data.get('child_age','')} years old</td>
        </tr>
        <tr>
          <td class="label">💰 Monthly Saving</td>
          <td class="value">RM {session_data.get('budget','')}</td>
        </tr>
        <tr>
          <td class="label">📘 Current Education Savings</td>
          <td class="value">{session_data.get('education_savings','None')}</td>
        </tr>
        <tr>
          <td class="label">📞 Phone</td>
          <td class="value">{session_data.get('phone','')}</td>
        </tr>
        <tr>
          <td class="label">📧 Email</td>
          <td class="value">{session_data.get('email','')}</td>
        </tr>
      </table>

      <!-- Projection -->
      <div class="projection">
        <p class="title">📈 Estimated Education Fund at Age 18</p>
        <p class="values">
          • 6% return: <strong>RM {calc_result['fv_6']:.2f}</strong><br>
          • 8% return: <strong>RM {calc_result['fv_8']:.2f}</strong><br>
          • 10% return: <strong>RM {calc_result['fv_10']:.2f}</strong>
        </p>
      </div>

      <!-- CTA -->
      <div class="cta">
        <a href="{whatsapp_link}" target="_blank">💬 Speak to an Education Advisor on WhatsApp</a>
      </div>

      <!-- Footer -->
      <div class="footer">
        <p>An authorised advisor may contact you to share suitable education planning options — no pressure, just helpful guidance 😊</p>
        <p>Warm regards,<br><strong>Education Planning Team</strong></p>
        <p>© {datetime.datetime.now().year} Education Planning. All rights reserved.</p>
      </div>
    </div>
  </div>
</body>
</html>
"""

        # Prepare and send email
        msg = MIMEMultipart()
        msg["From"] = FROM_EMAIL
        msg["To"] = to_email
        msg["Subject"] = SUBJECT
        msg.attach(MIMEText(body, "html"))

        # -----------------------------
        # Attach Benefits.pdf
        # -----------------------------
        filename = "Benefits.pdf"  # Change path if it's in a subfolder, e.g., "attachments/Benefits.pdf"
        if os.path.exists(filename):
            with open(filename, "rb") as f:
                part = MIMEBase("application", "pdf")
                part.set_payload(f.read())
                encoders.encode_base64(part)
                part.add_header(
                    "Content-Disposition",
                    f'attachment; filename="{os.path.basename(filename)}"',
                )
                msg.attach(part)
        else:
            logging.warning(f"Attachment {filename} not found. Email will be sent without it.")

        # Send email
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.send_message(msg)
        server.quit()

        logging.info(f"Campaign 2 email sent to {to_email}")
        return True

    except Exception:
        logging.exception("Failed to send Campaign 2 email")
        return False
