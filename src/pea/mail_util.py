import email

from bs4 import BeautifulSoup

from pea.auth import login


class Emails:
    def __init__(self):
        self.server = login()

    def get_mails(self, filter="UNSEEN", from_addr=None):
        self.server.select_folder("INBOX", readonly=True)
        if from_addr:
            selected_mails = self.server.search([filter, ["FROM", from_addr]])
        else:
            selected_mails = self.server.search([filter])
        return selected_mails

    def get_mails_content(self, selected_mails):
        mails_content = []
        for mail in selected_mails:
            mail_content = {}
            response = self.server.fetch(mail, "RFC822")
            email_data = response[mail][b"RFC822"]
            email_message = email.message_from_bytes(email_data)
            subject = email_message.get("Subject")
            from_addr = email_message.get("From")
            mail_content["from"] = from_addr
            mail_content["subject"] = subject

            body = None

            if email_message.is_multipart():
                for part in email_message.walk():
                    if part.get_content_type() == "text/plain":
                        body = part.get_payload(decode=True).decode(
                            part.get_content_charset(), errors="replace"
                        )
                        break
                    elif part.get_content_type() == "text/html":
                        html = part.get_payload(decode=True).decode(
                            part.get_content_charset(), errors="replace"
                        )
                        soup = BeautifulSoup(html, "html.parser")
                        body = soup.get_text()
                        break
            else:
                if email_message.get_content_type() == "text/plain":
                    body = email_message.get_payload(decode=True).decode(
                        email_message.get_content_charset(), errors="replace"
                    )
                elif email_message.get_content_type() == "text/html":
                    html = email_message.get_payload(decode=True).decode(
                        email_message.get_content_charset(), errors="replace"
                    )
                    soup = BeautifulSoup(html, "html.parser")
                    body = soup.get_text()

            if body:
                mail_content["body"] = "\n".join(
                    [line for line in body.splitlines() if line.strip()]
                )

            mails_content.append(mail_content)
        return mails_content
