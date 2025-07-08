import aiosmtplib
from email.message import EmailMessage

async def send_warning_mail(to_email, usage_percent, level="caution", suggestion=None, thinking_data=None):
    msg = EmailMessage()
    msg["From"] = "dharanidaran.a@winvinaya.com"
    msg["To"] = to_email

    # Set up the HTML content for the body
    html_body = f"""
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                color: #333;
                line-height: 1.6;
            }}
            .header {{
                background-color: #f4f4f4;
                padding: 10px;
                font-size: 18px;
                font-weight: bold;
            }}
            .content {{
                margin: 20px 0;
            }}
            .suggestions {{
                background-color: #e9f7ef;
                padding: 10px;
                border-left: 5px solid #28a745;
                margin: 10px 0;
            }}
            .suggestions ul {{
                list-style-type: none;
                padding-left: 0;
            }}
            .suggestions li {{
                margin: 5px 0;
                padding: 5px;
                background-color: #fff;
                border-radius: 3px;
            }}
            .thinking-data {{
                background-color: #f9f9f9;
                padding: 10px;
                border-left: 5px solid #007bff;
                margin: 10px 0;
            }}
        </style>
    </head>
    <body>
    """

    # If caution level, use simple text
    if level == "caution":
        msg["Subject"] = f"⚠️ Mailbox Usage Caution: {usage_percent:.2f}% Full"
        html_body += f"""
        <div class="header">Mailbox Storage Caution for {to_email}</div>
        <div class="content">
            <p>Your mailbox has reached {usage_percent:.2f}% of its allocated 500MB storage.</p>
            <p>Please consider cleaning up old or unnecessary emails soon to avoid interruption.</p>
        </div>
        """

    # If high alert level, add more detailed content with AI suggestions
    elif level == "high":
        msg["Subject"] = f"🚨 High Alert: Mailbox {usage_percent:.2f}% Full - Immediate Action Required"
        html_body += f"""
        <div class="header">Mailbox Storage Alert for {to_email}</div>
        <div class="content">
            <p>Your mailbox has reached a critical threshold of {usage_percent:.2f}% of 500MB storage.</p>
            <p>Please take immediate action to clear space or contact support for assistance to avoid email delivery issues.</p>
        </div>
        """

        # Add AI Suggested Cleanup Steps (if available)
        if suggestion:
            html_body += f"""
            <div class="suggestions">
                <b>AI Suggested Cleanup Steps:</b>
                <ul>
                    {''.join([f"<li>{line}</li>" for line in suggestion.split('<br>') if line.strip()])}
                </ul>
            </div>
            """

        # Add AI's Thought Process (if available)
        if thinking_data:
            html_body += f"""
            <div class="thinking-data">
                <b>AI's Thought Process:</b><br>
                <p>{thinking_data}</p>
            </div>
            """

    else:
        return  # Unknown level

    # Close the HTML tag and prepare the email body
    html_body += """
    <p>Thanks,</p>
    <p>WinVinaya Mailbox AI Agent</p>
    </body>
    </html>
    """

    # Set the HTML content as the email body
    msg.set_content("This is an HTML email, but your email client does not support HTML.", subtype="plain")
    msg.add_alternative(html_body, subtype="html")

    try:
        # Send the email using aiosmtplib
        await aiosmtplib.send(
            msg,
            hostname="s.mail25.info",
            port=587,
            start_tls=True,
            username="dharanidaran.a@winvinaya.com",
            password="Admin##2025",
        )
        print(f"📧 Alert ({level}) sent to {to_email}")
    except Exception as e:
        print(f"❌ Failed to send {level} alert to {to_email}: {e}")
