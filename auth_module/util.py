import httplib2
import pprint
import sys

from apiclient.discovery import build
from apiclient.errors import HttpError

from oauth2client.client import AccessTokenRefreshError
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client import tools

REDIRECT_URI = 'http://localhost:8000/auth/recieve_auth/'
PROJECT_NUMBER = 'lateral-replica-87221'

def refresh_credentials():

	FLOW = flow_from_clientsecrets(
		'client_secrets.json',
		scope='https://www.googleapis.com/auth/bigquery',
		redirect_uri=REDIRECT_URI)
  	auth_uri = FLOW.step1_get_authorize_url()

  	return auth_uri

def authorize(auth_code):
	FLOW = flow_from_clientsecrets(
		'client_secrets.json',
		scope='https://www.googleapis.com/auth/bigquery',
		redirect_uri=REDIRECT_URI)
	credentials = FLOW.step2_exchange(auth_code)
  	http_auth = credentials.authorize(httplib2.Http())
	return credentials
