import joblib
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
model = joblib.load('model.pkl')

def authenticate():
    flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
    creds = flow.run_local_server(port=0)
    service = build('gmail', 'v1', credentials=creds)
    return service

def fetch_emails(service):
    results = service.users().messages().list(userId='me', labelIds=['INBOX'], maxResults=5).execute()
    messages = results.get('messages', [])
    return messages

def classify_email(service, messages):
    for msg in messages:
        msg_data = service.users().messages().get(userId='me', id=msg['id']).execute()
        snippet = msg_data['snippet']
        label = model.predict([snippet])[0]
        print(f"EMAIL: {snippet[:60]}... → {'SPAM 🚫' if label else 'LEGIT ✅'}")

if __name__ == "__main__":
    service = authenticate()
    msgs = fetch_emails(service)
    classify_email(service, msgs)
