from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import os.path
import base64
import email
from bs4 import BeautifulSoup

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def getEmails():
 creds = None
 if os.path.exists('token.pickle'):
  with open('token.pickle', 'rb') as token:
   creds = pickle.load(token)
 if not creds or not creds.valid:
  if creds and creds.expired and creds.refresh_token:
   creds.refresh(Request())
  else:
   flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
   creds = flow.run_local_server(port=0)
  with open('token.pickle', 'wb') as token:
   pickle.dump(creds, token)
 service = build('gmail', 'v1', credentials=creds)
 result = service.users().messages().list(userId='me').execute()
 messages = result.get('messages')

 for msg in messages:
  txt = service.users().messages().get(userId='me', id=msg['id']).execute()

  try:
   payload = txt['payload']
   headers = payload['headers']

   for d in headers:
    if d['name'] == 'Subject':
     subject = d['value']
    if d['name'] == 'From':
     sender = d['value']

   parts = payload.get('parts')[0]
   data = parts['body']['data']
   data = data.replace("-","+").replace("_","/")
   decoded_data = base64.b64decode(data)
   soup = BeautifulSoup(decoded_data , "lxml")
   body = soup.body()
    
   print("Subject: ", subject)
   print("From: ", sender)
   print("Message: ", body)
   print('\n')
  except:
   pass

getEmails()
