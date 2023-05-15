from os import getenv


from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (
    Attachment,
    Disposition,
    FileContent,
    FileName,
    FileType,
    Mail,
)


class EmailReport:
    from_email: str = getenv("FROM_EMAIL")
    email_content = "<strong>New ports were found on your network!</strong>" #TODO - Configuration
    
    
    def send_report(self, report: str, user) -> bool:
        message = Mail(
            from_email=self.from_email,
            to_emails=user.email,
            subject="Email Report",
            html_content=self.email_content
        )
        
        attachment = Attachment(
            FileContent(report),
            FileName("attachment.txt"),
            FileType("text/plain"),
            Disposition("attachment")
        )
        message.attachment = attachment
        sg = SendGridAPIClient(api_key=getenv("SENDGRID_API_KEY"))
        response = sg.send(message)
        ## status_code is success
        return response.status_code in range(200, 300)
        