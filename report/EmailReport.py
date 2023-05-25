from os import getenv


from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (
    Mail,
)


class EmailReport:
    from_email: str = getenv("FROM_EMAIL")
    email_content = "<strong>New ports were found on your network!</strong>"
    
    @staticmethod
    def send_raw(to_email, from_email, subject, content) -> bool:
        message = Mail(
            from_email=EmailReport.from_email,
            to_emails=to_email,
            subject=subject,
            html_content=f"Email From: {from_email}<br>"+content
        )
        try:
            sg = SendGridAPIClient(api_key=getenv("SENDGRID_API_KEY"))
            response = sg.send(message)
        ## status_code is success
            return response.status_code in range(200, 300)
        except Exception as e:
            return False
    
    @staticmethod
    def send_report(report: str, user) -> bool:
        message = Mail(
            from_email=EmailReport.from_email,
            to_emails=user.email,
            subject="Email Report",
            html_content=EmailReport.email_content+report
        )
        
        
        try:
            sg = SendGridAPIClient(api_key=getenv("SENDGRID_API_KEY"))
            response = sg.send(message)
        ## status_code is success
            return response.status_code in range(200, 300)
        except Exception as e:
            return False
        