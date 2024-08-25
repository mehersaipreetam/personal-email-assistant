import email
from email.utils import parsedate_to_datetime

import yaml
from bs4 import BeautifulSoup
from langchain_core.tools import tool
from pydantic import BaseModel, Field

from mail import login


class GetMailContent(BaseModel):
    filter: str = Field(
        description="Filter on mails supported by IMAPClient like UNSEEN"
    )
    from_addr: str = Field(description="Sender's email address")


@tool("get_mails_content_tool", args_schema=GetMailContent)
def get_mails_content_tool(filter: str = "UNSEEN", from_addr: str = None):
    """
    Retrieve and parse the content of emails based on specified filters.

    Parameters
    ----------
    filter : str, optional
        The filter criteria for selecting emails. Default is "UNSEEN". Other possible values might include "SEEN", "ALL", etc.
    from_addr : str, optional
        The email address to filter by. If None, emails from all addresses are considered.

    Returns
    -------
    list of dict
        A list of dictionaries, each containing the following keys:
        - "from" : str
            The sender's email address.
        - "subject" : str
            The subject of the email.
        - "date_time" : str
            The date and time when the email was sent, in the format "YYYY-MM-DD HH:MM:SS TZ".
        - "body" : str, optional
            The plain text body of the email. If the email contains HTML, the text is extracted from the HTML.
    """
    email_obj = Emails()
    response = email_obj.get_mails_content(filter=filter, from_addr=from_addr)
    return response


class Emails:
    def __init__(self):
        self.server = login()
        with open("../config.yaml", "r") as file:
            self.config = yaml.safe_load(file)

    def _get_mails(self, filter, from_addr):
        self.server.select_folder("INBOX", readonly=True)
        if from_addr:
            selected_mails = self.server.search([filter, ["FROM", from_addr]])
        else:
            selected_mails = self.server.search([filter])
        return selected_mails

    def get_mails_content(self, filter: str = "UNSEEN", from_addr: str = None):
        """
        Retrieve and parse the content of emails based on specified filters.

        Parameters
        ----------
        filter : str, optional
            The filter criteria for selecting emails. Default is "UNSEEN". Other possible values might include "SEEN", "ALL", etc.
        from_addr : str, optional
            The email address to filter by. If None, emails from all addresses are considered.

        Returns
        -------
        list of dict
            A list of dictionaries, each containing the following keys:
            - "from" : str
                The sender's email address.
            - "subject" : str
                The subject of the email.
            - "date_time" : str
                The date and time when the email was sent, in the format "YYYY-MM-DD HH:MM:SS TZ".
            - "body" : str, optional
                The plain text body of the email. If the email contains HTML, the text is extracted from the HTML.
        """
        selected_mails = self._get_mails(filter, from_addr)
        num_mails = len(selected_mails)
        num_mails = (
            num_mails
            if num_mails < self.config["mail_length"]
            else self.config["mail_length"]
        )
        selected_mails = selected_mails[-num_mails:]
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

            date_tuple = email.utils.parsedate_tz(email_message["Date"])
            if date_tuple:
                email_date = parsedate_to_datetime(email_message["Date"])
                mail_content["date_time"] = email_date.strftime("%Y-%m-%d %H:%M:%S %Z")

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