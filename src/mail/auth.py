import os

from dotenv import load_dotenv
from imapclient import IMAPClient


def login():
    load_dotenv()
    EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
    EMAIL_APP_PASSWORD = os.getenv("EMAIL_APP_PASSWORD")
    EMAIL_HOST = os.getenv("EMAIL_HOST")
    server = IMAPClient(EMAIL_HOST, use_uid=True)
    _ = server.login(EMAIL_ADDRESS, EMAIL_APP_PASSWORD)
    return server
