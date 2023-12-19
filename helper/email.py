import resend

def sent_email(sender: str | None, to: str, body: dict) -> bool:
    try:
        resend.api_key = "re_g2z8DreF_AJxToFAUcCLRLsG53eFKpdUg"
        resend.Emails.send({
            "from": "admin@reportmanagement.online" if sender else sender,
            "to": to,
            "subject": "Report Management System",
            "html": f"<p>Hello {body.get('username')},<p><p>Email: <strong>{body.get('email')}</strong></p><p>Password: <strong>{body.get('password')}</strong></p><p>Our Website: <strong>reportmanagement.online</strong></p>"
        })
        return True
    except:
        return False