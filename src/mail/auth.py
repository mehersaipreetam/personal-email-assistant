import os

from dotenv import load_dotenv
from imapclient import IMAPClient


def login():
    """
    Logs into an email server using credentials stored in environment variables 
    and returns an authenticated IMAPClient session.

    Returns
    -------
    IMAPClient
        An authenticated instance of IMAPClient connected to the email server.
    """
    load_dotenv()
    EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
    EMAIL_APP_PASSWORD = os.getenv("EMAIL_APP_PASSWORD")
    EMAIL_HOST = os.getenv("EMAIL_HOST")
    server = IMAPClient(EMAIL_HOST, use_uid=True)
    _ = server.login(EMAIL_ADDRESS, EMAIL_APP_PASSWORD)
    return server
