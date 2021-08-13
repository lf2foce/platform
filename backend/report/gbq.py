"""GMAIL Credentials Auth."""
import os
import sys
# import httplib2
import pickle
import base64
from datetime import datetime
import google.auth
# from googleapiclient import discovery, errors
from google.cloud import bigquery
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
# import mimetypes


SCOPES = ["https://www.googleapis.com/auth/bigquery"]
CLIENT_SECRET_FILE = 'client_cred.json'
APPLICATION_NAME = os.getenv('APPLICATION_NAME', 'BigQuery API Wrapper')

class GoogleConnection:
    """An API connection establisher for Google APIs."""

    def __init__(self):
        """Google API connection establisher.
        """
        self.scopes = SCOPES
        self._get_credentials()

    def _get_bool_value(self, value):
        """Return bool value from string."""
        bool_list = ['True', 'true', 'Yes', 'yes']
        return True if value in bool_list else False

    def _get_connection_flags(self):
        """Get connection flags."""
        try:
            import argparse
            flags = argparse.ArgumentParser(
                parents=[tools.argparser]).parse_args()
        except (ImportError,):
            flags = None
        return flags

    def _get_credentials(self):
        """Get valid user credentials from storage.

        If nothing has been stored, or if the stored credentials are invalid,
        the OAuth2 flow is completed to obtain the new credentials.

        Returns:
            Credentials, the obtained credential.
        """
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        home_dir = os.path.expanduser('~')
        token_dir = os.path.join(home_dir, '.credentials')
        if not os.path.exists(token_dir):
            os.makedirs(token_dir)
        token_path = os.path.join(token_dir,'token_bq.pickle')
        if os.path.exists(token_path):
            with open(token_path, 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    CLIENT_SECRET_FILE, self.scopes)
                flow.user_agent = APPLICATION_NAME
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(token_path, 'wb') as token:
                pickle.dump(creds, token)
        self.credentials = creds


class BQConnection(GoogleConnection):
    """BigQuery API connection."""
    def __init__(self, project):
        """BigQuery connection establisher.
        """
        GoogleConnection.__init__(self)
        self.project = project
        self.bq_api_connect()

    def bq_api_connect(self):
        """Get BigQuery service.

        Get authenticated to the BigQuery API.
        """
        client = bigquery.Client(credentials=self.credentials, project=self.project)
        self.client = client


def main():
    bqcon = BQConnection(project='vinid-data-selfservice-prod')
    query = 'select id from vinid-data-selfservice-prod.SNG_MM_MART.F_ORDERS limit 1000'
    bqcon.client
    quey_job = bqcon.client.query(query)
    df = quey_job.to_dataframe()
    print(df)

if __name__ == '__main__':
    main()

